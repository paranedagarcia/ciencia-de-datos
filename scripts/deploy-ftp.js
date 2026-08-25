const ftp = require('basic-ftp')
const fs = require('fs')
const path = require('path')

function loadDotEnv(filePath = '.env') {
  if (!fs.existsSync(filePath)) return
  const content = fs.readFileSync(filePath, 'utf8')
  for (const line of content.split(/\r?\n/)) {
    const trimmed = line.trim()
    if (!trimmed || trimmed.startsWith('#')) continue
    const eq = trimmed.indexOf('=')
    if (eq === -1) continue
    const key = trimmed.slice(0, eq).trim()
    const val = trimmed.slice(eq + 1).trim().replace(/^"|"$/g, '')
    if (!process.env[key]) process.env[key] = val
  }
}

loadDotEnv()

const FTP_HOST = process.env.FTP_HOST
const FTP_USER = process.env.FTP_USER
const FTP_PASSWORD = process.env.FTP_PASSWORD
const FTP_PORT = process.env.FTP_PORT ? parseInt(process.env.FTP_PORT, 10) : 21
const FTP_SECURE_RAW = (process.env.FTP_SECURE || 'false').trim().toLowerCase()
const FTP_REMOTE_PATH = process.env.FTP_REMOTE_PATH || '/'
const FTP_SECURE_SERVERNAME = process.env.FTP_SECURE_SERVERNAME
const FTP_SECURE_REJECT_UNAUTHORIZED =
  (process.env.FTP_SECURE_REJECT_UNAUTHORIZED || 'true').trim().toLowerCase() !== 'false'

function resolveSecureMode(value) {
  if (value === 'true' || value === 'explicit') return true
  if (value === 'implicit') return 'implicit'
  return false
}

function buildAccessOptions(overrides = {}) {
  const secureOptions = {
    minVersion: 'TLSv1.2',
    maxVersion: 'TLSv1.2',
    rejectUnauthorized: FTP_SECURE_REJECT_UNAUTHORIZED,
    servername: FTP_SECURE_SERVERNAME || FTP_HOST,
    ...(overrides.secureOptions || {})
  }

  return {
    host: FTP_HOST,
    port: FTP_PORT,
    user: FTP_USER,
    password: FTP_PASSWORD,
    secure: resolveSecureMode(FTP_SECURE_RAW),
    ...overrides,
    secureOptions,
  }
}

function shouldRetryWithImplicitFtps(err) {
  const message = String(err && err.message ? err.message : err).toLowerCase()
  return message.includes('cleartext sessions') || message.includes('tls security mechanisms')
}

function shouldRetryWithoutCertificateValidation(err) {
  return err && err.code === 'ERR_TLS_CERT_ALTNAME_INVALID'
}

if (!FTP_HOST || !FTP_USER || !FTP_PASSWORD) {
  console.error('Missing FTP configuration. Please set FTP_HOST, FTP_USER, FTP_PASSWORD.')
  process.exit(1)
}

async function uploadDir(client, localDir, remoteDir) {
  const items = await fs.promises.readdir(localDir, { withFileTypes: true })
  await client.ensureDir(remoteDir)
  for (const item of items) {
    const localPath = path.join(localDir, item.name)
    const remotePath = path.posix.join(remoteDir, item.name)
    if (item.isDirectory()) {
      await uploadDir(client, localPath, remotePath)
    } else if (item.isFile()) {
      await client.uploadFrom(localPath, remotePath)
      //console.log('Uploaded', localPath, '->', remotePath)
      console.log('Uploaded', remotePath)
    }
  }
}

async function connectClient(client) {
  try {
    await client.access(buildAccessOptions())
  } catch (err) {
    if (!shouldRetryWithImplicitFtps(err) || FTP_SECURE_RAW === 'implicit') {
      throw err
    }

    client.close()
    console.warn('Explicit FTPS was rejected by the server. Retrying with implicit FTPS.')
    await client.access(
      buildAccessOptions({
        secure: 'implicit',
        port: FTP_PORT === 21 ? 990 : FTP_PORT,
      })
    )
  }
}

async function deployBuild(client) {
  const localBuild = path.resolve(__dirname, '..', 'build')
  if (!fs.existsSync(localBuild)) {
    console.error('Local build folder not found:', localBuild)
    process.exit(1)
  }

  console.log('Starting upload of', localBuild, 'to', FTP_HOST, FTP_REMOTE_PATH)
  await uploadDir(client, localBuild, FTP_REMOTE_PATH)
  console.log('Upload complete')
}

;(async () => {
  const client = new ftp.Client()
  client.ftp.verbose = false
  try {
    await connectClient(client)
    await deployBuild(client)
  } catch (err) {
    if (shouldRetryWithoutCertificateValidation(err) && FTP_SECURE_REJECT_UNAUTHORIZED) {
      try {
        client.close()
        console.warn(
          'The FTP server certificate does not match the configured host. Retrying with certificate validation disabled.'
        )
        await client.access(
          buildAccessOptions({
            secureOptions: {
              minVersion: 'TLSv1.2',
              rejectUnauthorized: false,
              servername: FTP_SECURE_SERVERNAME || FTP_HOST,
            },
          })
        )

        await deployBuild(client)
        return
      } catch (retryErr) {
        console.error('FTP upload failed:', retryErr)
        process.exitCode = 1
        return
      }
    }

    console.error('FTP upload failed:', err)
    process.exitCode = 1
  } finally {
    client.close()
  }
})()
