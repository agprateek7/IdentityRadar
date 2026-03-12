/*
  Warnings:

  - You are about to drop the column `userId` on the `ScanJob` table. All the data in the column will be lost.
  - You are about to drop the column `lastCheckImage` on the `Site` table. All the data in the column will be lost.
  - You are about to drop the `CrawledImage` table. If the table is not empty, all the data it contains will be lost.
  - Added the required column `siteId` to the `ScanJob` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "CrawledImage" DROP CONSTRAINT "CrawledImage_siteId_fkey";

-- DropForeignKey
ALTER TABLE "ScanJob" DROP CONSTRAINT "ScanJob_userId_fkey";

-- AlterTable
ALTER TABLE "Match" ADD COLUMN     "pageUrl" TEXT;

-- AlterTable
ALTER TABLE "ScanJob" DROP COLUMN "userId",
ADD COLUMN     "errorMessage" TEXT,
ADD COLUMN     "imagesFound" INTEGER NOT NULL DEFAULT 0,
ADD COLUMN     "matchesFound" INTEGER NOT NULL DEFAULT 0,
ADD COLUMN     "siteId" TEXT NOT NULL,
ADD COLUMN     "startedAt" TIMESTAMP(3);

-- AlterTable
ALTER TABLE "Site" DROP COLUMN "lastCheckImage",
ADD COLUMN     "crawlInterval" INTEGER NOT NULL DEFAULT 60,
ADD COLUMN     "isActive" BOOLEAN NOT NULL DEFAULT true;

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "updatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- DropTable
DROP TABLE "CrawledImage";

-- AddForeignKey
ALTER TABLE "ScanJob" ADD CONSTRAINT "ScanJob_siteId_fkey" FOREIGN KEY ("siteId") REFERENCES "Site"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
