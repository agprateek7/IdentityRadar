import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient()

async function main() {
    const url = "https://www.reddit.com"
    await prisma.site.upsert({
      where: { url: url },
      update: {subreddit: "pics"},
      create: {
        name: "Reddit",
        url: url,
        crawlInterval: 60,
        isActive: true,
        subreddit: "pics"
      },
    });
}

main()
    .catch(console.error)
    .finally(() => prisma.$disconnect())