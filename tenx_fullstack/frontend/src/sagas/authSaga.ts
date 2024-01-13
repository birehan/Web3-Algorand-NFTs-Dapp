import { PayloadAction } from '@reduxjs/toolkit'
import { call, put, takeLatest } from 'redux-saga/effects'
import Auths from '../api/auth'
import { AuthType } from '../interfaces/types'
import { LoginErrorAction, LoginSuccessAction } from '../redux/authSlice'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function* userLogin({ payload: user }: PayloadAction<AuthType>): Generator<any, void, AuthType> {
  try {
    const data = yield call(Auths.login, user)
    yield put(LoginSuccessAction(data))
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    yield put(LoginErrorAction(error?.response?.data?.error || 'Something went wrong! try again'))
  }
}

export function* watchUserLogin() {
  yield takeLatest('auth/LoginAction', userLogin)
}
