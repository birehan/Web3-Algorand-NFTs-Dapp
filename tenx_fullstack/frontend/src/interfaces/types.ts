export interface ApiResponse<T> {
  isSuccess: boolean
  value: T | null
  error: string | null
}

export interface LoginUser {
  username: string
  password: string
}

export interface AuthType {
  email: string
  password: string
}
