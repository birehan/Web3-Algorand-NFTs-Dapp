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

export interface Certificate {
  challenge_id: number
  id: number
  ipfs_hash: string
  is_approved: 'NoRequest' | 'Pending' | 'Approved' | 'Denied'
  issued_date: string
  nft_id: string
  score: number
  staff_id: number
  title: string
  user_id: number
}

export interface CreateCertificate {
  user_id: number
  challenge_id: number
  certificate_name: string
}
