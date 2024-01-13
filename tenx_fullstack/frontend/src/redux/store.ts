import createSagaMiddleware from '@redux-saga/core'
import { configureStore } from '@reduxjs/toolkit'
import { createLogger } from 'redux-logger'; // Import the createLogger function

import { persistStore } from 'redux-persist'
import rootSaga from '../sagas/rootSaga'
import rootReducers from './rootReducers'

const sagaMiddleware = createSagaMiddleware()

export const store = configureStore({
  reducer: rootReducers,
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(sagaMiddleware, createLogger()), // Add logger
})

export const persistor = persistStore(store)

sagaMiddleware.run(rootSaga)
