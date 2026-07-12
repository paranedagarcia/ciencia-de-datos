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
const FTP_SECURE = (process.env.FTP_SECURE || 'false').toLowerCase() === 'true'
const FTP_REMOTE_PATH = process.env.FTP_REMOTE_PATH || '/'

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

;(async () => {
  const client = new ftp.Client()
  client.ftp.verbose = false
  try {
    await client.access({
      host: FTP_HOST,
      port: FTP_PORT,
      user: FTP_USER,
      password: FTP_PASSWORD,
      secure: FTP_SECURE,
    })

    const localBuild = path.resolve(__dirname, '..', 'build')
    if (!fs.existsSync(localBuild)) {
      console.error('Local build folder not found:', localBuild)
      process.exit(1)
    }

    console.log('Starting upload of', localBuild, 'to', FTP_HOST, FTP_REMOTE_PATH)
    await uploadDir(client, localBuild, FTP_REMOTE_PATH)
    console.log('Upload complete')
  } catch (err) {
    console.error('FTP upload failed:', err)
    process.exitCode = 1
  } finally {
    client.close()
  }
})()
