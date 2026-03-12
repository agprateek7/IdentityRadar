import cron from 'node-cron'
import { PrismaClient } from '@prisma/client'
import { addScanJob } from '../queues/scanQueue.js'

const prisma = new PrismaClient()

const scanScheduler = cron.schedule('0 * * * *', async() => {
    console.log('[Scheduler] Cron fired at', new Date().toISOString())
    const sites = await prisma.site.findMany({
        where: {isActive: true}
    })
    console.log(`[Scheduler] Found ${sites.length} active sites`)
    
    for(const site of sites){
        console.log(`[Scheduler] Queuing job for site: ${site.url}, subreddit: ${site.subreddit}`)
        await addScanJob(site.subreddit, site.url)
    }
})

export default scanScheduler