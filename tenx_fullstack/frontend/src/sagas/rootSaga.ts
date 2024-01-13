import { all } from 'redux-saga/effects'
import { watchUserLogin } from './authSaga'

export default function* rootSaga() {
  yield all([watchUserLogin()])
}
