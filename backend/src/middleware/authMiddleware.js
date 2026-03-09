import jwt from "jsonwebtoken";
import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

const protect = async (req, res, next) => {
    try {
        const authHeader = req.headers.authorization;
        //console.log(req);
        if(!authHeader || !authHeader.startsWith('Bearer')) {
            return res.status(401).json({
                message: "Token Missing"
            });
        }
        const token = authHeader.split(' ')[1];
        const decoded = jwt.verify(token, process.env.JWT_ACCESS_SECRET);
        req.user = await prisma.user.findUnique({
            where: {id: decoded.id},
            select: {id: true, name: true, email: true}
        })
        next();
    } catch (error) {
        res.status(401).json({message: "Invalid or expired token", error: error.message})
    }
}

export {protect};