import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
// import AlumniList from '../components/AlumniList'
import { FaExternalLinkAlt } from 'react-icons/fa'
import { IoCloseSharp } from 'react-icons/io5'
import Modal from 'react-modal'
import { Link } from 'react-router-dom'
import Loading from '../components/Loading'
import { Certificate } from '../interfaces/types'
import { FetchAllCertificates, UpdateCertificateAction } from '../redux/certificateSlice'

const Certificates = () => {
  const dispatch = useDispatch()
  const { loading, certificates } = useSelector((state: any) => state.certificates)
  const { user } = useSelector((state: any) => state.auth)

  const [isModalOpen, setIsModalOpen] = useState(false)

  const openModal = () => {
    setIsModalOpen(true)
  }

  const closeModal = () => {
    setIsModalOpen(false)
  }

  const [password, setPassword] = useState('')

  useEffect(() => {
    dispatch(FetchAllCertificates())
  }, [dispatch])

  if (loading) {
    return <Loading />
  }

  const customStyles = {
    overlay: {
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
    },
    content: {
      position: 'absolute',
      top: '55%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      maxWidth: '80%',
      overflow: 'auto',
      borderRadius: '8px',
      height: '87%',
    },
  }

  const handleActions = (id: string, path: string) => {
    // Display an alert to insert the password
    const userInputPassword = prompt('Please enter your password:')

    if (userInputPassword !== null) {
      // Save the password to state
      setPassword(userInputPassword)
      // Dispatch the action with the provided password
      dispatch(UpdateCertificateAction({ path: path, id: id, password: userInputPassword }))
      setPassword('')
    } else {
      // Handle the case where the user pressed Cancel in the prompt
      // You can decide how to handle this case based on your requirements
      alert('Password input canceled.')
    }
  }

  const handleTransfer = (id: string) => {
    // Display an alert to insert the password
    const userInputPassword = prompt('Please enter your password:')

    if (userInputPassword !== null) {
      // Save the password to state
      setPassword(userInputPassword)
      // Dispatch the action with the provided password
      dispatch(UpdateCertificateAction({ path: 'optin/approve', id: id, password: userInputPassword }))
      setPassword('')
    } else {
      // Handle the case where the user pressed Cancel in the prompt
      // You can decide how to handle this case based on your requirements
      alert('Password input canceled.')
    }
  }

  return (
    <div className="mx-auto max-w-[100rem] flex flex-col gap-6 ">
      <div className="flex flex-row justify-between items-center gap-4">
        <h3 className="text-primaryColor text-2xl font-bold">Certificates</h3>

        {user?.role === 'Issuer' && (
          <Link to="/user/register">
            <button
              type="button"
              className=" inline-flex justify-center items-center  gap-x-1.5 rounded-md bg-primaryColor px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primaryColorHover focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primaryColorHover"
            >
              Create Certificate
            </button>
          </Link>
        )}
      </div>

      <div id="scroll">
        <div>
          <div className="mb-8 xl:mb-16  max-w-[70rem] flex flex-col gap-8 md:gap-24  ">
            <table className="min-w-full divide-y divide-gray-200 overflow-x-auto">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Certificate ID
                  </th>

                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>

                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Issue Date
                  </th>

                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Certificate
                  </th>

                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Approval Status
                  </th>

                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {certificates.map((certificate: Certificate, index: number) => {
                  // Split the date string into components
                  const dateComponents = certificate.issued_date.split(' ')

                  // Format the date to "Sat, 13 Jan 2024"
                  const formattedDate = `${dateComponents[0]} ${dateComponents[2]} ${dateComponents[1]}, ${dateComponents[3]}`

                  return (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap flex flex-center">
                        <div className="text-sm font-medium text-gray-900">{certificate.id}</div>
                      </td>

                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{certificate.title}</td>

                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formattedDate}</td>

                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {/* {certificate.is_approved === 'Approved' ? <FaExternalLinkAlt color="" /> : <FaExternalLinkAlt color="" />} */}

                        {certificate.is_approved === 'Approved' ? (
                          <>
                            <FaExternalLinkAlt color="#00cc00" onClick={openModal} />

                            <Modal isOpen={isModalOpen} onRequestClose={closeModal} style={customStyles}>
                              <div style={{ position: 'relative' }}>
                                <img
                                  src={`https://gateway.pinata.cloud/ipfs/${certificate.ipfs_hash}`}
                                  alt="Certificate Image"
                                  style={{ width: '100%', height: 'auto' }}
                                />
                                <button
                                  onClick={closeModal}
                                  style={{
                                    position: 'absolute',
                                    top: '10px',
                                    right: '10px',
                                    padding: '8px',
                                    cursor: 'pointer',
                                    backgroundColor: '#fff',
                                    border: '1px solid #ddd',
                                    borderRadius: '4px',
                                  }}
                                >
                                  <IoCloseSharp />
                                </button>
                              </div>
                            </Modal>
                          </>
                        ) : (
                          <FaExternalLinkAlt color="#808080" />
                        )}
                      </td>

                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{certificate.is_approved}</td>

                      <td className="px-6 py-4 whitespace-nowrap  text-sm font-medium">
                        {/* <Link to={`/user/update/${curUser.id}`} className="text-indigo-600 hover:text-indigo-900">
                          Edit
                        </Link> */}
                        {certificate.is_approved === 'NoRequest' && user?.role == 'Trainee' && (
                          <button
                            onClick={() => handleActions(certificate.id.toString(), 'optin')}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-4 rounded"
                          >
                            {loading ? <span className="loading loading-spinner" /> : 'OptIn'}
                          </button>
                        )}

                        {(certificate.is_approved === 'Approved' || certificate.is_approved === 'Pending') && user?.role == 'Trainee' && (
                          <button
                            onClick={() => handleActions(certificate.id.toString(), 'optin')}
                            className="bg-[#840303] hover:bg-[#9a2323] text-white font-bold py-1 px-4 rounded"
                          >
                            {loading ? <span className="loading loading-spinner" /> : 'OptOut'}
                          </button>
                        )}

                        {(certificate.is_approved === 'Pending' || certificate.is_approved === 'Approved') && user?.role == 'Issuer' && (
                          <div className="flex flex-row gap-2">
                            <button
                              onClick={() => handleActions(certificate.id.toString(), 'optin/approve')}
                              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-4 rounded"
                            >
                              {loading ? <span className="loading loading-spinner" /> : 'Transfer'}
                            </button>
                            <button
                              onClick={() => handleActions(certificate.id.toString(), 'optin/approve')}
                              className="bg-[#840303] hover:bg-[#9a2323] text-white font-bold py-1 px-4 rounded"
                            >
                              {loading ? <span className="loading loading-spinner" /> : 'Revoke'}
                            </button>
                          </div>
                        )}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Certificates
