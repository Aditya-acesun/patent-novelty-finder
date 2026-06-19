import { User, IUser } from '../models/user.model';
import { signToken } from '../config/jwt';

interface RegisterInput {
  name: string;
  email: string;
  password: string;
  role?: 'admin' | 'researcher' | 'viewer';
}

interface LoginInput {
  email: string;
  password: string;
}

interface AuthResponse {
  token: string;
  user: {
    id: string;
    name: string;
    email: string;
    role: string;
  };
}

export async function registerUser(input: RegisterInput): Promise<AuthResponse> {
  const { name, email, password, role = 'researcher' } = input;

  // Check if user already exists
  const existing = await User.findOne({ email });
  if (existing) {
    throw new Error('Email already registered');
  }

  const user = await User.create({ name, email, password, role });

  const token = signToken({
    userId: user._id.toString(),
    email: user.email,
    role: user.role,
  });

  return {
    token,
    user: {
      id: user._id.toString(),
      name: user.name,
      email: user.email,
      role: user.role,
    },
  };
}

export async function loginUser(input: LoginInput): Promise<AuthResponse> {
  const { email, password } = input;

  // Get user with password field (normally excluded)
  const user = await User.findOne({ email }).select('+password');
  if (!user || !user.isActive) {
    throw new Error('Invalid email or password');
  }

  const isMatch = await user.comparePassword(password);
  if (!isMatch) {
    throw new Error('Invalid email or password');
  }

  const token = signToken({
    userId: user._id.toString(),
    email: user.email,
    role: user.role,
  });

  return {
    token,
    user: {
      id: user._id.toString(),
      name: user.name,
      email: user.email,
      role: user.role,
    },
  };
}

export async function getMe(userId: string): Promise<Partial<IUser>> {
  const user = await User.findById(userId).select('-password');
  if (!user) throw new Error('User not found');
  return user;
}
