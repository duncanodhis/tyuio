/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react'
import {
  CButton,
  CForm,
  CFormInput,
  CFormTextarea,
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableDataCell,
} from '@coreui/react'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import Token from './Token'
const Newsletter = () => {
  const [message, setMessage] = useState('')
  const [newsletters, setNewsletters] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)
  const [showPreview, setShowPreview] = useState(false)
  const [expandedMessage, setExpandedMessage] = useState(null)

  const handleSend = async () => {
    // Create a new FormData object to handle multipart/form-data
    const formData = new FormData()
    formData.append('message', message)

    // Append the selected file to the FormData if it exists
    if (selectedFile) {
      formData.append('file', selectedFile)
    }

    try {
      // Make a POST request to your server's endpoint with the FormData
      const response = await fetch('http://localhost:5000/api/newsletters', {
        method: 'POST',
        body: formData, // Use the FormData object as the request body
      })

      if (response.ok) {
        // Show a success toast
        toast.success('Message sent successfully!', {
          autoClose: 5000,
          position: 'top-right',
        })

        // Reset the message and file input
        setMessage('')
        setSelectedFile(null)
      } else {
        // Handle the case when the request fails (e.g., show an error toast)
        console.error('Failed to send message')
        toast.error('Failed to send message', {
          autoClose: 5000,
          position: 'top-right',
        })
      }
    } catch (error) {
      // Handle any errors that may occur during the request (e.g., network issues)
      console.error('An error occurred while sending the message', error)
      toast.error('An error occurred while sending the message', {
        autoClose: 5000,
        position: 'top-right',
      })
    }
  }
  useEffect(() => {
    async function fetchNewsletters() {
      try {
        const response = await fetch('http://localhost:5000/api/newsletters')
        if (response.ok) {
          const data = await response.json()
          setNewsletters(data) // Update the newsletters state with the fetched data
        } else {
          console.error('Failed to fetch newsletters')
          toast.error('Failed to fetch newsletters', {
            autoClose: 5000,
            position: 'top-right',
          })
        }
      } catch (error) {
        console.error('An error occurred while fetching newsletters', error)
        toast.error('An error occurred while fetching newsletters', {
          autoClose: 5000,
          position: 'top-right',
        })
      }
    }

    fetchNewsletters()
  }, [])

  const handlePreview = () => {
    setShowPreview(!showPreview)
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    setSelectedFile(file)
  }

  const handleDelete = async (newsletterId) => {
    try {
      // Send a delete request to your server's delete endpoint with the newsletterId
      const response = await fetch(`http://localhost:5000/api/newsletters/${newsletterId}`, {
        method: 'DELETE', // Use the appropriate HTTP method (DELETE in this case)
      })

      if (response.ok) {
        // Show a success toast
        toast.success('Newsletter deleted successfully!', {
          autoClose: 5000,
          position: 'top-right',
        })

        // Remove the deleted newsletter from the local state
        const updatedNewsletters = newsletters.filter(
          (newsletter) => newsletter.id !== newsletterId,
        )
        setNewsletters(updatedNewsletters)
      } else {
        // Handle the case when the delete request fails (e.g., show an error toast)
        console.error('Failed to delete newsletter')
        toast.error('Failed to delete newsletter', {
          autoClose: 5000,
          position: 'top-right',
        })
      }
    } catch (error) {
      console.error('An error occurred while deleting the newsletter', error)
      toast.error('An error occurred while deleting the newsletter', {
        autoClose: 5000,
        position: 'top-right',
      })
    }
  }
  const handleChangeMessage = (e) => {
    setMessage(e.target.value)
  }

  return (
   
    <div>
     <div>
      <Token/>
    </div>
      <ToastContainer position="top-right" autoClose={5000} />
      <h1>Newsletter</h1>
      <div>
      </div>
      <CForm>
      <div>
      <CFormTextarea
          id="message"
          rows={3}
          text="Must be less than 600 words long."
          value={message}
          onChange={handleChangeMessage}
        ></CFormTextarea>
        <CFormInput
          type="file"
          id="file"
          label="Select a file (optional)"
          onChange={handleFileChange}
        />
        <CButton color="primary" onClick={handleSend}>
          Send
        </CButton>
      </div>
      </CForm>

      {showPreview && (
        <div>
          <h2>Preview:</h2>
          <p>{message}</p>
          {selectedFile && (
            <div>
              <p>File: {selectedFile.name}</p>
              <img
                src={URL.createObjectURL(selectedFile)}
                alt="Preview"
                style={{ maxWidth: '100%', maxHeight: '300px' }}
              />
            </div>
          )}
        </div>
      )}

      <CTable>
        <CTableHead>
          <CTableRow>
            <CTableHeaderCell scope="col">Date</CTableHeaderCell>
            <CTableHeaderCell scope="col">Message</CTableHeaderCell>
            <CTableHeaderCell scope="col">Actions</CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <tbody>
          {newsletters.map((newsletter, index) => (
            <CTableRow key={newsletter.id}>
              <CTableDataCell>
                {new Date(newsletter.created_at).toLocaleDateString()}
              </CTableDataCell>
              <CTableDataCell>
                {expandedMessage === index ? (
                  <div>
                    <p>{newsletter.message}</p>
                    {newsletter.file && (
                      <div>
                        <p>File: {newsletter.file}</p>
                        <img
                          src={`http://localhost:5000/uploads/${newsletter.file}`}
                          alt="Preview"
                          style={{ maxWidth: '100%', maxHeight: '300px' }}
                        />
                      </div>
                    )}
                  </div>
                ) : (
                  <div>
                    <p>{newsletter.message.substring(0, 100)}...</p>
                    <CButton color="info" size="sm" onClick={() => setExpandedMessage(index)}>
                      Read More
                    </CButton>
                  </div>
                )}
              </CTableDataCell>
              <CTableDataCell>

                <CButton color="info" onClick={handlePreview}>
                  Preview
                </CButton>
                <CButton color="danger" onClick={() => handleDelete(newsletter.id)}>
                  Delete
                </CButton>
              </CTableDataCell>
            </CTableRow>
          ))}
        </tbody>
      </CTable>
    </div>
  )
}

export default Newsletter
