import express from 'express'
import { createMatch } from '../controllers/matchController.js';
const router = express.Router();

router.post('/internal/matches', createMatch)

export {router}