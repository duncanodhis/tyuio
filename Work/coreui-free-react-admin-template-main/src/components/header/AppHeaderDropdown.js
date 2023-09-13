// import React from 'react'
// import {
//   CAvatar,
//   CDropdown,
//   CDropdownHeader,
//   CDropdownItem,
//   CDropdownMenu,
//   CDropdownToggle,
//   CButton,
// } from '@coreui/react'
// // import { NavLink } from 'react-router-dom'
// import avatar8 from './../../assets/images/avatars/8.jpg'
// import Signup from '../signup/Signup'
// const AppHeaderDropdown = () => {
//   return (
//     <CDropdown variant="nav-item">
//       <CDropdownToggle placement="bottom-end" className="py-0" caret={false}>
//         <CAvatar src={avatar8} size="md" />
//       </CDropdownToggle>
//       <CDropdownMenu className="pt-0" placement="bottom-end">
//         <CDropdownHeader className="bg-light fw-semibold py-2">Account</CDropdownHeader>
//         <CDropdownItem href="#">
//           <CButton>Signout</CButton>
//         </CDropdownItem>
//         <CDropdownItem>
//           <Signup />
//         </CDropdownItem>
//       </CDropdownMenu>
//     </CDropdown>
//   )
// }

// export default AppHeaderDropdown
import React, { useState } from 'react'
import {
  CAvatar,
  CDropdown,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
  CButton,
} from '@coreui/react'
import avatar8 from './../../assets/images/avatars/9.jpg'
import Signup from '../signup/Signup'
const AppHeaderDropdown = () => {
  // Step 2: Create a state variable for user authentication
  const [isLoggedIn, setIsLoggedIn] = useState(true)

  // Step 3: Function to handle logout
  const handleLogout = () => {
    // Perform logout actions (e.g., clearing tokens, redirecting, etc.)
    // You should update this logic based on your authentication setup
    // Example: clear user tokens from local storage
    // localStorage.removeItem('userToken')

    // Update the authentication state
    setIsLoggedIn(false)

    // Redirect the user to the login page after logout
    window.location.href = '/login'
  }

  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0" caret={false}>
        <CAvatar src={avatar8} size="md" />
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader className="bg-light fw-semibold py-2">Account</CDropdownHeader>
        {isLoggedIn ? (
          <CDropdownItem>
            <CButton onClick={handleLogout}>Signout</CButton>
          </CDropdownItem>
        ) : null}
        <CDropdownItem>
          {/* Your signup component */}
          <Signup />
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  )
}

export default AppHeaderDropdown
