import { combineReducers } from 'redux'
import { persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import authSlice from './authSlice'
import { certificateslice } from './certificateSlice'

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['auth', 'certificates'],
}

const rootReducer = combineReducers({
  auth: authSlice.reducer,
  certificates: certificateslice.reducer,
})
const rootReducers = persistReducer(persistConfig, rootReducer)

export default rootReducers
