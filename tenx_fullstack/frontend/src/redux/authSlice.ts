import { PayloadAction, createSlice } from '@reduxjs/toolkit'
import { AuthType } from '../../interfaces/types'

export type authState = {
  user: AuthType | null
  isLoading: boolean
  error: string
  isLoggingSuccess: boolean
}
const authInitialState: authState = {
  user: null,
  isLoading: false,
  error: '',
  isLoggingSuccess: false,
}

export const authSlice = createSlice({
  name: 'auth',
  initialState: authInitialState,
  reducers: {
    LoginAction: (state: authState, { payload: user }: PayloadAction<AuthType>) => {
      state.isLoading = true
      state.error = ''
      state.user = null
    },
    LoginSuccessAction: (state: authState, { payload: user }: PayloadAction<AuthType>) => {
      state.isLoggingSuccess = true
      state.user = user
    },
    LoginErrorAction: (state: authState, { payload: error }: PayloadAction<string>) => {
      state.isLoading = false
      state.error = error
      state.isLoggingSuccess = false
    },

    LogOutAction: (state: authState) => {
      state.user = null
    },

    CleanStatusAuth: (state: { isLoading: boolean; isLoggingSuccess: boolean; error: string }) => {
      state.isLoading = false
      state.isLoggingSuccess = false
      state.error = ''
    },
  },
})

export const {
  LoginAction,
  LoginSuccessAction,
  LoginErrorAction,

  LogOutAction,
  CleanStatusAuth,
} = authSlice.actions

export default authSlice
