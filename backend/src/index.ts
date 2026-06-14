import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import { connectDB } from './config/database';
import { setupSwagger } from './swagger/swagger';
import authRoutes from './routes/auth.routes';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

// ── Middleware ──────────────────────────────────────────
app.use(helmet());
app.use(cors({ origin: process.env.FRONTEND_URL || '*', credentials: true }));
app.use(express.json({ limit: '10mb' }));
app.use(morgan('dev'));

// ── Swagger Docs ────────────────────────────────────────
setupSwagger(app);

// ── Routes ──────────────────────────────────────────────
app.use('/api/auth', authRoutes);

// ── Health Check ────────────────────────────────────────
app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok', service: 'patent-novelty-backend', ts: new Date() });
});

// ── Start ───────────────────────────────────────────────
connectDB().then(() => {
  app.listen(PORT, () => {
    console.log(`✅ Backend running on http://localhost:${PORT}`);
    console.log(`📄 Swagger docs at http://localhost:${PORT}/api/docs`);
  });
});

export default app;
