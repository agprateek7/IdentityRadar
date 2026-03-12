import { Queue } from "bullmq";
import { redisConfig } from "../config/redis.js";

const scanQueue = new Queue("site-scan", { connection: redisConfig });

export async function addScanJob(subreddit, site_url) {
  await scanQueue.add(
    "scan",
    {
      subreddit,
      site_url,
    },
    {
      attempts: 3, // retry up to 3 times on failure
      backoff: { type: "exponential", delay: 5000 },
    },
  );
}
