import { useEffect } from 'react'
import { FormProvider, SubmitHandler, useForm } from 'react-hook-form'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import PasswordInput from '../components/PasswordInput'
import SubmitButton from '../components/SubmitButton'
import TextInput from '../components/TextInput'
// import PasswordInput from '../inputs/PasswordInput'
import Notification from '../components/Notification'
import { LoginUser } from '../interfaces/types'
import { CleanStatusAuth, LoginAction } from '../redux/authSlice'

export default function Login() {
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const { isLoading, isLoggingSuccess, error } = useSelector((state: any) => state.auth)

  const methods = useForm<LoginUser>()

  const onSubmit: SubmitHandler<LoginUser> = (data) => {
    dispatch(LoginAction(data))
  }

  useEffect(() => {
    if (isLoggingSuccess) {
      setTimeout(() => {
        navigate('/')
      }, 2000)
    }
    return () => {}
  }, [isLoggingSuccess])

  useEffect(() => {
    return () => {
      dispatch(CleanStatusAuth())
    }
  }, [])

  return (
    <FormProvider {...methods}>
      <div className="flex min-h-full flex-1 flex-col justify-center py-12 sm:px-6 lg:px-8">
        {isLoggingSuccess && <Notification success={isLoggingSuccess} message="Logged in succesffully" />}

        {error && <Notification success={isLoggingSuccess} message={error} />}

        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <img className="mx-auto h-10 w-auto" src="src/assets/10x_logo.png" alt="Your Company" />
          <h2 className="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
        </div>

        <div className="mt-10 mx-auto sm:w-full sm:max-w-[480px]">
          <div className="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12  mx-auto">
            <form className="space-y-6 mx-auto w-full" onSubmit={methods.handleSubmit(onSubmit)}>
              <TextInput label={'Username'} name={'username'} />
              <PasswordInput label={'Password'} name={'password'} />

              <div className="flex items-center justify-between">
                <div className="flex items-center"></div>

                <div className="text-sm leading-6">
                  <Link to="/auth/forgetpassword" className="font-semibold text-primaryColor hover:text-primaryColorHover">
                    Don't have accout, <button></button>
                  </Link>
                </div>
              </div>
              <div className="text-center">
                <SubmitButton text=" Sign in" isLoading={isLoading}></SubmitButton>
              </div>
            </form>
          </div>
        </div>
      </div>
    </FormProvider>
  )
}
