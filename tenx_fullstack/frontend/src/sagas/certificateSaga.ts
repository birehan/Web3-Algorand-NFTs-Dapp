import { PayloadAction } from '@reduxjs/toolkit'
import { call, put, takeLatest } from 'redux-saga/effects'
import Certificates from '../api/certificates'
import { Certificate, CreateCertificate } from '../interfaces/types'
import {
  CreateCertificateFailure,
  CreateCertificateSuccess,
  FetchAllCertificatesFailure,
  FetchAllCertificatesSuccess,
  UpdateCertificateFailure,
  UpdateCertificateSuccess,
} from '../redux/certificateSlice'

function* fetchAllCertificates({}: PayloadAction<Certificate[]>): Generator<any, void, Certificate[]> {
  try {
    const data = yield call(Certificates.list)
    yield put(FetchAllCertificatesSuccess(data))
  } catch (error) {
    yield put(FetchAllCertificatesFailure('Something went wrong'))
  }
}

function* createCertificate({ payload: Certificate }: PayloadAction<CreateCertificate>): Generator<any, void, Certificate> {
  try {
    const data = yield call(Certificates.create, Certificate)
    yield put(CreateCertificateSuccess(data))
  } catch (error: any) {
    yield put(CreateCertificateFailure(error?.response?.data?.error || 'Something went wrong! try again'))
  }
}

function* updateCertificate({
  payload: { path, id, password },
}: PayloadAction<{ path: string; id: string; password: string }>): Generator<any, void, Certificate> {
  try {
    const data = yield call(Certificates.update, path, id, password) // Assuming Certificates.update is your API call for updating Certificate
    yield put(UpdateCertificateSuccess(data))
  } catch (error: any) {
    yield put(UpdateCertificateFailure(error?.response?.data?.error || 'Something went wrong! try again'))
  }
}

export function* CertificateSaga() {
  yield takeLatest('certificates/FetchAllCertificates', fetchAllCertificates)
  yield takeLatest('certificates/CreateCertificateAction', createCertificate)
  yield takeLatest('certificates/UpdateCertificateAction', updateCertificate)
}
