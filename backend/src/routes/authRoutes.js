import express from 'express'
import { registerUser, loginUser, getUser, refresh } from '../controllers/authController.js'
import {protect} from '../middleware/authMiddleware.js'

const router = express.Router()

router.post('/register', registerUser)
router.post('/login', loginUser)
router.post('/refresh', refresh)
router.get('/me', protect, getUser)

export {router}