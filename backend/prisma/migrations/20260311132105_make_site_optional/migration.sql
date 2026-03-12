-- DropForeignKey
ALTER TABLE "CrawledImage" DROP CONSTRAINT "CrawledImage_siteId_fkey";

-- AlterTable
ALTER TABLE "CrawledImage" ALTER COLUMN "siteId" DROP NOT NULL;

-- AddForeignKey
ALTER TABLE "CrawledImage" ADD CONSTRAINT "CrawledImage_siteId_fkey" FOREIGN KEY ("siteId") REFERENCES "Site"("id") ON DELETE SET NULL ON UPDATE CASCADE;
