import { LoginUser } from '../interfaces/types'
import { requests } from './request'

const Auths = {
  login: (user: LoginUser) => requests.post<LoginUser>('/login', user),
}

export default Auths
