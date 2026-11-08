const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const test = require('node:test')
const vm = require('node:vm')

const script = fs.readFileSync(path.join(__dirname, 'deploy-ftp.js'), 'utf8')

async function runConnection(secure, errors) {
  const calls = []
  const messages = []
  const processStub = {
    env: { FTP_HOST: 'ftp.example.com', FTP_USER: 'user', FTP_PASSWORD: 'password', FTP_PORT: '21', FTP_SECURE: secure },
    exitCode: 0,
    exit(code) { this.exitCode = code },
  }
  class Client {
    constructor() { this.ftp = {} }
    async access(options) {
      calls.push(options)
      throw errors[calls.length - 1]
    }
    close() {}
  }
  const context = {
    require(name) {
      if (name === 'basic-ftp') return { Client }
      if (name === 'fs') return { existsSync: () => false }
      return require(name)
    },
    console: { log() {}, warn(...args) { messages.push(args.join(' ')) }, error(...args) { messages.push(args.join(' ')) } },
    process: processStub,
    __dirname,
  }
  await vm.runInNewContext(script, context)
  return { calls, messages, exitCode: processStub.exitCode }
}

test('retries a rejected plaintext session with explicit FTPS on the configured port', async () => {
  const result = await runConnection('false', [new Error('Cleartext sessions are not accepted'), new Error('stop')])
  assert.equal(result.calls.length, 2)
  assert.equal(result.calls[1].secure, true)
  assert.equal(result.calls[1].port, 21)
  assert.equal(result.calls[1].secureOptions.rejectUnauthorized, true)
})

test('does not switch an explicitly secure connection to implicit FTPS', async () => {
  const result = await runConnection('true', [new Error('TLS security mechanisms required')])
  assert.equal(result.calls.length, 1)
  assert.equal(result.exitCode, 1)
})

test('reports certificate hostname mismatch without disabling validation', async () => {
  const error = Object.assign(new Error('hostname mismatch'), { code: 'ERR_TLS_CERT_ALTNAME_INVALID' })
  const result = await runConnection('true', [error])
  assert.equal(result.calls.length, 1)
  assert.equal(result.exitCode, 1)
  assert.ok(result.messages.some(message => message.includes('certificate does not match')))
})