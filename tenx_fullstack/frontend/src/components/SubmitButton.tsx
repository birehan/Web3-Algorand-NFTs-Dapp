interface Props {
  text: string
  isLoading: boolean
}

const SubmitButton = ({ text, isLoading }: Props) => {
  return (
    <button
      disabled={isLoading}
      type="submit"
      className="w-full max-w-[16rem] mx-auto text-center inline-flex justify-center items-center gap-x-1.5 rounded-md bg-primaryColor px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primaryColorHover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primaryColorHover"
    >
      {isLoading ? (
        <div className="flex items-center justify-center ">
          <div className="w-6 h-6 border-b-2 border-white rounded-full animate-spin"></div>
        </div>
      ) : (
        text
      )}
    </button>
  )
}

export default SubmitButton
