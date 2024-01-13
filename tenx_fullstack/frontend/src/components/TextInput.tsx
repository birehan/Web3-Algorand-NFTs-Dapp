import React from 'react'
import { useFormContext } from 'react-hook-form'

interface Props {
  label: string
  name: string
}

const TextInput: React.FC<Props> = ({ name, label }) => {
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
          type="text"
          {...register(name, {
            required: true,
          })}
          className="block w-full px-2 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primaryColorHover sm:text-sm sm:leading-6"
        />

        {errors[name]?.type === 'required' && (
          <p className="text-red-500" role="alert">
            {label} is required
          </p>
        )}
      </div>
    </div>
  )
}

export default TextInput
