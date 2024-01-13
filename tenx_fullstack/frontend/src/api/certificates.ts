import { Certificate, CreateCertificate } from '../interfaces/types'
import { requests } from './request'

const Certificates = {
  list: () => requests.get<Certificate[]>('/certificates'),

  create: (certificate: CreateCertificate) => requests.post<Certificate>('/certificates', certificate),

  update: (path: string, id: string, password: string) => requests.put<Certificate>(`/certificates/${path}/${id}`, { password: password }),
}

export default Certificates
