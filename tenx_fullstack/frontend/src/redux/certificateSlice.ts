import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { Certificate } from '../interfaces/types'

export interface CertificateState {
  certificates: Certificate[]
  certificate: Certificate | null
  isLoading: boolean
  error: string | null
  isCreateSuccess: boolean
  isUpdateSuccess: boolean
  isDeleteSuccess: boolean
}

const initialState: CertificateState = {
  certificate: null,
  certificates: [],
  isLoading: false,
  error: null,
  isCreateSuccess: false,
  isUpdateSuccess: false,
  isDeleteSuccess: false,
}

export const certificateslice = createSlice({
  name: 'certificates',
  initialState,
  reducers: {
    FetchAllCertificates: (state) => {
      state.isLoading = true
      state.error = null
      state.certificates = []
    },
    FetchAllCertificatesSuccess: (state, action: PayloadAction<Certificate[]>) => {
      state.isLoading = false
      state.certificates = action.payload
    },
    FetchAllCertificatesFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false
      state.error = action.payload
    },

    CreateCertificateAction: (state, { payload: certificate }: PayloadAction<Certificate>) => {
      state.isLoading = true
      state.error = ''
      state.isCreateSuccess = false
    },

    CreateCertificateSuccess: (state, action: PayloadAction<Certificate>) => {
      state.isLoading = false
      state.certificates = [...state.certificates, action.payload]
      state.error = ''
      state.isCreateSuccess = true
    },
    CreateCertificateFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false
      state.error = action.payload
      state.isCreateSuccess = false
    },

    UpdateCertificateAction: (state, { payload }: PayloadAction<{ path: string; id: string; password: string }>) => {
      state.isLoading = true
      state.error = ''
      state.isUpdateSuccess = false
    },

    UpdateCertificateSuccess: (state, action: PayloadAction<Certificate>) => {
      state.isLoading = false
      state.certificate = action.payload
      state.error = ''
      state.isUpdateSuccess = true
      state.certificates = state.certificates.map((alumni) => (alumni.id === action.payload.id ? action.payload : alumni))
    },
    UpdateCertificateFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false
      state.error = action.payload
      state.isUpdateSuccess = false
    },

    CleanUpCertificate: (state) => {
      state.isLoading = false
      state.error = ''
      state.isCreateSuccess = false
      state.isUpdateSuccess = false
      state.isDeleteSuccess = false
      state.certificate = null
      state.certificates = []
    },

    CleanUpStatusCertificate: (state) => {
      state.isLoading = false
      state.error = ''
      state.isCreateSuccess = false
      state.isUpdateSuccess = false
      state.isDeleteSuccess = false
    },
  },
})

export const {
  FetchAllCertificates,
  FetchAllCertificatesSuccess,
  FetchAllCertificatesFailure,
  CreateCertificateAction,
  CreateCertificateSuccess,
  CreateCertificateFailure,
  UpdateCertificateAction,
  UpdateCertificateSuccess,
  UpdateCertificateFailure,
  CleanUpCertificate,
  CleanUpStatusCertificate,
} = certificateslice.actions
