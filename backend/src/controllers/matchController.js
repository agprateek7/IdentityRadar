import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient()

const createMatch = async (req, res) => {
    try {
        // Bug fix 1: was "idenity" (typo)
        const identity = await prisma.identity.findUnique({
          where: { id: req.body.identity_id },
        });

        if (!identity) {
          return res.status(404).json({ message: "Identity not found" });
        }

        // Bug fix 3: "reddit" is not a valid Site ID (it's a FK).
        // We upsert a Site record so "reddit" always exists before we reference it.

        const site = await prisma.site.findUnique({
          where: { url: req.body.site_url }
        });

        if (!site) {
          return res
            .status(404)
            .json({ message: "Site not found. Make sure it is seeded." });
        }

        const match = await prisma.match.create({
          data: {
            imageUrl: req.body.image_url,
            pageUrl: req.body.page_url,
            confidenceScore: req.body.score,
            identityId: req.body.identity_id, // Bug fix 2: was "identity_id" (undefined)
            siteId: site.id,
            status: "NEW",
          },
        });

        await prisma.alert.create({
          data: {
            userId: identity.userId,
            matchId: match.id,
          },
        });

        res.status(200).json({
          message: "Alert match found",
        });
    } catch(error) {
        res.status(500).json({
            message: 'Server error',
            error: error.message
        })
    }
}

export {createMatch}