/* eslint-disable prettier/prettier */
import React, { useState } from 'react'
import {
  CButton,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CModalTitle,
  CForm,
  CFormLabel,
  CFormInput,
  CToast,
  CToastHeader,
  CToastBody,
} from '@coreui/react'

const Signup = () => {
  const [visible, setVisible] = useState(false)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [toastVisible, setToastVisible] = useState(false)
  const [toastMessage, setToastMessage] = useState('')
  const [toastType, setToastType] = useState('success')

  const showToast = (message, type) => {
    setToastMessage(message)
    setToastType(type)
    setToastVisible(true)
  }

  const handleSaveChanges = () => {
    // Send the email and password to your backend or API endpoint
    // Replace the API_URL with your actual backend URL
    const API_URL = 'http://127.0.0.1:5000/api/signup'

    // Prepare the data to send to the server
    const formData = new FormData()
    formData.append('username', username)
    formData.append('email', email)
    formData.append('password', password)

    // Send the POST request to your server
    fetch(API_URL, {
      method: 'POST',
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          // Signup was successful, close the modal and show success toast
          setVisible(false)
          showToast('Signup successful', 'success')
        } else {
          // Handle signup failure, show an error message or toast
          console.error('Signup failed')
          showToast('Signup failed', 'danger')
        }
      })
      .catch((error) => {
        console.error('Error:', error)
        // Handle network errors and show an error toast
        showToast('Network error', 'danger')
      })
  }

  return (
    <>
      <CButton onClick={() => setVisible(!visible)}>Sign up</CButton>
      <CModal alignment="center" visible={visible} onClose={() => setVisible(false)}>
        <CModalHeader>
          <CModalTitle>Sign Up</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CForm>
            <CFormLabel htmlFor="email">Username</CFormLabel>
            <CFormInput
              type="text"
              id="username"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <CFormLabel htmlFor="email">Email</CFormLabel>
            <CFormInput
              type="email"
              id="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <CFormLabel htmlFor="password">Password</CFormLabel>
            <CFormInput
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </CForm>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setVisible(false)}>
            Close
          </CButton>
          <CButton color="primary" onClick={handleSaveChanges}>
            Save changes
          </CButton>
        </CModalFooter>
      </CModal>
      <CToast
        show={toastVisible}
        color={toastType === 'success' ? 'success' : 'danger'}
        autohide={3000} // Adjust the duration as needed
        onClose={() => setToastVisible(false)}
      >
        <CToastHeader closeButton>{toastMessage}</CToastHeader>
        <CToastBody>{toastType === 'success' ? 'Signup successful' : 'Signup failed'}</CToastBody>
      </CToast>
    </>
  )
}

export default Signup
