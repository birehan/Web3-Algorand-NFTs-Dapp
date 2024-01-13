import { Disclosure } from '@headlessui/react'
import { ChevronRightIcon } from '@heroicons/react/20/solid'
import { UsersIcon } from '@heroicons/react/24/outline'
import { useState } from 'react'
import { GrCertificate } from 'react-icons/gr'
import { useSelector } from 'react-redux'
import { Link, useLocation } from 'react-router-dom'

const navigation = [{ name: 'Certificates', href: '/', icon: GrCertificate, current: false }]

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ')
}
const DesktopSidebar = () => {
  const location = useLocation()
  const { user } = useSelector((state: any) => state.auth)
  const [navigationLinks, setnavigationLinks] = useState<any>(navigation)

  if (user !== null && user.userRole === 'SuperAdmin' && navigation[navigation.length - 1].name !== 'Users') {
    navigation.push({
      name: 'Users',
      href: '/users',
      icon: UsersIcon,
      current: false,
    })
  }

  return (
    <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
      <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6 pb-4">
        <div>
          <div className="flex h-16 shrink-0 items-center">
            <img className="h-8 w-auto" src="src/assets/10x_logo.png" alt="Your Company" />
          </div>
          <div>{user?.role} Account</div>
        </div>

        <nav className="flex flex-1 flex-col">
          <ul role="list" className="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" className="-mx-2 space-y-1">
                {navigation.map((item) => {
                  return (
                    <li key={item.name}>
                      {!item.children ? (
                        <Link
                          to={item.href}
                          className={classNames(
                            item.current ? 'bg-gray-50 text-indigo-600' : 'text-gray-700 hover:text-indigo-600 hover:bg-gray-50',
                            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold',
                          )}
                        >
                          <item.icon
                            className={classNames(
                              item.current ? 'text-indigo-600' : 'text-gray-400 group-hover:text-indigo-600',
                              'h-6 w-6 shrink-0',
                            )}
                            aria-hidden="true"
                          />
                          {item.name}
                        </Link>
                      ) : (
                        <Disclosure as="div">
                          {({ open }) => (
                            <>
                              <Link to={location.pathname.startsWith('/staff') ? '#' : item.href}>
                                <Disclosure.Button
                                  className={classNames(
                                    item.current ? 'bg-gray-50' : 'hover:bg-gray-50',
                                    'flex items-center w-full text-left rounded-md p-2 gap-x-3 text-sm leading-6 font-semibold text-gray-700',
                                  )}
                                >
                                  <ChevronRightIcon
                                    className={classNames(open ? 'rotate-90 text-gray-500' : 'text-gray-400', 'h-5 w-5 shrink-0')}
                                    aria-hidden="true"
                                  />

                                  {item.name}
                                </Disclosure.Button>
                              </Link>
                              <Disclosure.Panel as="ul" className="mt-1 px-2">
                                {item.children.map((subItem) => (
                                  <Link key={subItem.name} to={subItem.href}>
                                    <li>
                                      <Disclosure.Button
                                        className={classNames(
                                          subItem.current ? 'bg-gray-50' : 'hover:bg-gray-50',
                                          'block rounded-md py-2 pr-2 pl-9 text-sm leading-6 text-gray-700',
                                        )}
                                      >
                                        {subItem.name}
                                      </Disclosure.Button>
                                    </li>
                                  </Link>
                                ))}
                              </Disclosure.Panel>
                            </>
                          )}
                        </Disclosure>
                      )}
                    </li>
                  )
                })}
              </ul>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  )
}

export default DesktopSidebar
