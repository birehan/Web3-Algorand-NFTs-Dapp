// import createSagaMiddleware from '@redux-saga/core'
// import { configureStore } from '@reduxjs/toolkit'
// import { createLogger } from 'redux-logger'; // Import the createLogger function
// import { persistStore } from 'redux-persist'
// import rootSaga from '../sagas/rootSaga'
// import rootReducers from './rootReducers'

// const loggerMiddleware = createLogger() // Create the logger middleware
// const sagaMiddleware = createSagaMiddleware()

// const middlewares = []
// middlewares.push(sagaMiddleware)

// if (process.env.NODE_ENV === 'development') {
//   middlewares.push(loggerMiddleware)
// }

// export const store = configureStore({
//   reducer: rootReducers,
//   middleware: [loggerMiddleware],
// })

// export const persistor = persistStore(store)

// sagaMiddleware.run(rootSaga)

// import createSagaMiddleware from '@redux-saga/core'
// import { configureStore } from '@reduxjs/toolkit'
// import { persistStore } from 'redux-persist'
// import rootSaga from '../sagas/rootSaga'
// import rootReducers from './rootReducers'

// const sagaMiddleware = createSagaMiddleware()

// export const store = configureStore({
//   reducer: rootReducers,
//   middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(sagaMiddleware), // Apply sagaMiddleware
// })

// export const persistor = persistStore(store)

// sagaMiddleware.run(rootSaga) // Run sagas after store configuration

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
