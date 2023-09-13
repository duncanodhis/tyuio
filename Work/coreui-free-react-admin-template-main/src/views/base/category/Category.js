/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import {
  CForm,
  CFormInput,
  CFormFeedback,
  CCol,
  CButton,
  CContainer,
  CTooltip,
} from '@coreui/react'

const Category = () => {
  const [categories, setCategories] = useState([])
  const [newCategory, setNewCategory] = useState('')
  const [validated, setValidated] = useState(false)

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/categories')
        const fetchedCategories = response.data // Assuming the API returns an array of categories
        setCategories(fetchedCategories)
      } catch (error) {
        // Handle any errors that occurred during the API call
        console.error('Error fetching categories:', error)
      }
    }
    fetchCategories()
  }, [])

  const handleInputChange = (event) => {
    setNewCategory(event.target.value)
  }

  const handleAddCategory = async (event) => {
    event.preventDefault()
    const form = event.currentTarget

    if (form.checkValidity() === false) {
      event.stopPropagation()
    } else {
      if (newCategory.trim() !== '') {
        try {
          const response = await axios.post('http://127.0.0.1:5000/api/categories', {
            name: newCategory,
          })
          const savedCategory = response.data // Assuming the API returns the saved category object with an ID
          setCategories([...categories, savedCategory])
          setNewCategory('')
        } catch (error) {
          // Handle any errors that occurred during the API call
          console.error('Error saving category:', error)
        }
      }
    }
    setValidated(true)
  }

  return (
    <CContainer>
      <h2>Create Category</h2>
      <CForm
        className="row g-3 needs-validation"
        noValidate
        validated={validated}
        onSubmit={handleAddCategory}
      >
        <CCol md={4}>
          <CFormInput
            type="text"
            value={newCategory}
            onChange={handleInputChange}
            placeholder="Enter category name"
            required
          />
          <CFormFeedback invalid>Please enter a category name.</CFormFeedback>
        </CCol>
        <CCol md={12}>
          <CTooltip
            content="You need to create a category for your product
              e.g category shoe then the product can be Sneakers,Boots,Loafers.. even high heels
              .If you already created then check it in the view section below 👇!
              Then Smile 😊"
            placement="right"
          >
            <CButton color="primary" type="submit">
              Add Category
            </CButton>
          </CTooltip>
        </CCol>
      </CForm>

      <h2>View Categories</h2>
      {categories.length === 0 ? (
        <p>No categories available.</p>
      ) : (
        <ul>
          {categories.map((category) => (
            <li key={category.id}>{category.name}</li>
          ))}
        </ul>
      )}
    </CContainer>
  )
}

export default Category
