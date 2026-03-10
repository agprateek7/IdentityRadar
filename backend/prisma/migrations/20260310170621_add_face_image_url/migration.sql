/*
  Warnings:

  - Added the required column `faceImageUrl` to the `Identity` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Identity" ADD COLUMN     "faceImageUrl" TEXT NOT NULL;
