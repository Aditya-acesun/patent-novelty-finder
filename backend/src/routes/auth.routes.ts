import { Router } from 'express';
// Controllers will be added in Phase 2
const router = Router();

/**
 * @swagger
 * /api/auth/register:
 *   post:
 *     summary: Register a new user
 *     tags: [Auth]
 */
router.post('/register', (_req, res) => {
  res.json({ message: 'Phase 2: register endpoint – coming soon' });
});

/**
 * @swagger
 * /api/auth/login:
 *   post:
 *     summary: Login and receive JWT
 *     tags: [Auth]
 */
router.post('/login', (_req, res) => {
  res.json({ message: 'Phase 2: login endpoint – coming soon' });
});

export default router;
