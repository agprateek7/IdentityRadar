import dotenv from 'dotenv'
dotenv.config();
import express from 'express';
import cors from 'cors'
import cookieParser from 'cookie-parser';
import {router as authRoutes} from './src/routes/authRoutes.js'
import {router as identityRoutes} from './src/routes/identityRoutes.js'

const app = express();

app.use(
  cors({
    origin: "*",
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: ["Content-Type", "Authorization"],
  }),
);

app.use(express.json());
app.use(cookieParser())

app.use('/api/auth', authRoutes);
app.use('/api/identity', identityRoutes)

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`)
})