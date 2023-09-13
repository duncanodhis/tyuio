import React, { useState } from 'react'
import axios from 'axios'
import { CForm, CFormInput, CButton } from '@coreui/react'
import { toast, ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

function Wallet() {
  const [walletAddress, setWalletAddress] = useState('')
  const [isDisabled, setIsDisabled] = useState(false)

  const handleInputChange = (e) => {
    setWalletAddress(e.target.value)
  }

  const handleSubmit = () => {
    // console.log(walletAddress)
    // Send the wallet address to the endpoint using axios or your preferred HTTP library
    axios
      .post('http://localhost:5000/api/create_payment_wallet', { walletAddress })
      .then((response) => {
        // Handle the response if needed
        // console.log('Wallet address sent successfully:', response.data)
        // Show a success toast
        toast.success('Wallet address sent successfully')
      })
      .catch((error) => {
        // Handle errors here
        console.error('Error sending wallet address:', error)
        // Show an error toast
        toast.error('Error sending wallet address')
      })

    // Clear the input value
    setWalletAddress('')
  }

  const toggleDisabled = () => {
    // Toggle the disabled state
    setIsDisabled(!isDisabled)
  }

  return (
    <div>
      <CForm>
        <CFormInput
          type="text"
          placeholder="Enter Bitcoin Wallet Address"
          value={walletAddress}
          onChange={handleInputChange}
          disabled={isDisabled}
        />
        <CButton color="primary" onClick={handleSubmit} disabled={!walletAddress || isDisabled}>
          Send
        </CButton>
      </CForm>
      <CButton color="info" onClick={toggleDisabled}>
        {isDisabled ? 'Enable Input' : 'Disable Input'}
      </CButton>
      <ToastContainer position="top-right" autoClose={3000} />
    </div>
  )
}

export default Wallet
