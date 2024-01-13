import React from 'react'
import { useFormContext } from 'react-hook-form'

interface Props {
  label: string
  name: string
}

const PasswordInput: React.FC<Props> = ({ name, label }) => {
  const {
    register,
    formState: { errors },
  } = useFormContext()

  return (
    <div className="flex-1">
      <label htmlFor={name} className="block text-sm font-medium leading-6 text-gray-900">
        {label}
      </label>
      <div className="mt-2">
        <input
          id={name}
          type="password"
          autoComplete="current-password"
          {...register(name, {
            required: `${name} is required`,
            minLength: {
              value: 4,
              message: `${name} must be at least 4 characters long`,
            },
          })}
          className="block w-full px-2 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primaryColorHover sm:text-sm sm:leading-6"
        />

        <p className="text-red-500 text-sm mt-1">{errors[name] && errors[name]?.message ? String(errors[name]?.message) : null}</p>
      </div>
    </div>
  )
}

export default PasswordInput
