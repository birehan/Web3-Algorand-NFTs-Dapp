import { all } from 'redux-saga/effects'
import { watchUserLogin } from './authSaga'
import { CertificateSaga } from './certificateSaga'

export default function* rootSaga() {
  yield all([watchUserLogin(), CertificateSaga()])
}
