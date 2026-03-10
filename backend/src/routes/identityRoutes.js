import express from 'express'
import { saveIdentity } from '../controllers/identityController.js'
import { protect } from '../middleware/authMiddleware.js'
import multer from "multer";

const upload = multer({ storage: multer.memoryStorage() });
const router = express.Router()

router.post("/upload", protect, upload.single("face"), saveIdentity);

export {router}