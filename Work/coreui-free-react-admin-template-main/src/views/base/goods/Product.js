/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableDataCell,
  CCollapse,
  CCard,
  CCardBody,
  CTableBody,
  CFormInput,
//   CImage,
  CListGroup,
  CListGroupItem,
  CInputGroup,
  CInputGroupText,
  CFormTextarea,
  CButton,
} from '@coreui/react'

  
const ProductTable = () => {
  const [products, setProducts] = useState([])
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [editingProduct, setEditingProduct] = useState(null)

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/products')
      setProducts(response.data)
    } catch (error) {
      console.error('Error fetching products:', error)
    }
  }

  const toggleCollapse = (product) => {
    if (selectedProduct && selectedProduct.id === product.id) {
      setSelectedProduct(null)
    } else {
      setSelectedProduct(product)
    }
  }

  const deleteProduct = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/products/${id}`)
      fetchProducts()
    } catch (error) {
      console.error('Error deleting product:', error)
    }
  }

  const editProduct = (product) => {
    setEditingProduct(product)
    toggleCollapse(product)
  }

  const saveEditedProduct = async () => {
    try {
      const formData = new FormData();
      formData.append('package_price', editingProduct.package_price);
      formData.append('package_currency', editingProduct.package_currency);
      formData.append('selling_price', editingProduct.selling_price);
      formData.append('selling_weight', editingProduct.selling_weight);
      formData.append('selling_weight_measurement', editingProduct.selling_weight_measurement);
      formData.append('package_description', editingProduct.package_description);
      formData.append('country', editingProduct.country);
      formData.append('city', editingProduct.city);
      formData.append('district', editingProduct.district);
    
      // Check if an image file is selected, and if so, append it
      if (editingProduct.imageFile) {
        formData.append('image', editingProduct.imageFile);
      }
  
      await axios.put(`http://127.0.0.1:5000/api/products/${editingProduct.id}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        });

  
      fetchProducts();
      setEditingProduct(null);
    } catch (error) {
      console.error('Error editing product:', error);
    }
  };
  

  const cancelEdit = () => {
    setEditingProduct(null)
  }
//   const generateImageURL = (imagePath) => {
//     // Replace backslashes with forward slashes in the image path
//     const normalizedImagePath = imagePath.replace(/\\/g, '/');
//     // Construct the full image URL using the server's base URL and the normalized image path
//     const fullImageURL = `http://127.0.0.1:5000${normalizedImagePath}`;
//     return fullImageURL;
//   };

  return (
    <>
      <CTable>
        <CTableHead>
          <CTableRow>
            <CTableHeaderCell>Name</CTableHeaderCell>
            <CTableHeaderCell>Actions</CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
        {products.map((product) => (
            <CTableRow key={product.id}>
            <CTableDataCell>{product.name}</CTableDataCell>
            <CTableDataCell className="d-flex justify-content-between align-items-center">
                <div>
                <CButton onClick={() => toggleCollapse(product)}>View</CButton>
                </div>
                <div>
                <CButton color="info" onClick={() => editProduct(product)}>
                    Edit
                </CButton>
                </div>
                <div>
                <CButton color="danger" onClick={() => deleteProduct(product.id)}>
                    Delete
                </CButton>
                </div>
            </CTableDataCell>
            </CTableRow>
        ))}
        </CTableBody>
      </CTable>
      <CTableBody>
</CTableBody>
      {selectedProduct && (
        <CCollapse visible={selectedProduct !== null}>
            <CCard className="mt-3">
            <CCardBody>
            {/* <div className="clearfix">
                <CImage
                    align="center"
                    rounded
                    src={generateImageURL(selectedProduct.package_image)}
                    alt="Product image"
                    width={200}
                    height={200}
                />
                </div> */}
                <CListGroup>
                <CListGroupItem active>{selectedProduct.name}</CListGroupItem>
                <CListGroupItem>Package Price: {selectedProduct.package_price}</CListGroupItem>
                <CListGroupItem>Package Currency: {selectedProduct.package_currency}</CListGroupItem>
                <CListGroupItem>Package Weight: {selectedProduct.package_weight}</CListGroupItem>
                <CListGroupItem>
                    Package Weight Measurement: {selectedProduct.package_weight_measurement}
                </CListGroupItem>
                <CListGroupItem>Selling Price: {selectedProduct.selling_price}</CListGroupItem>
                <CListGroupItem>Selling Currency: {selectedProduct.selling_currency}</CListGroupItem>
                <CListGroupItem>Selling Weight: {selectedProduct.selling_weight}</CListGroupItem>
                <CListGroupItem>
                    Selling Weight Measurement: {selectedProduct.selling_weight_measurement}
                </CListGroupItem>
                <CListGroupItem>Country: {selectedProduct.country}</CListGroupItem>
                <CListGroupItem>City: {selectedProduct.city}</CListGroupItem>
                <CListGroupItem>District: {selectedProduct.district}</CListGroupItem>
                </CListGroup>
            </CCardBody>
            </CCard>
        </CCollapse>
        )}
        {editingProduct && (
  <CCollapse visible={true}>
    <CCard className="mt-3">
      <CCardBody>
        <h3>Edit Product: {editingProduct.name}</h3>
        <form>
          <CInputGroup className="mb-3">
            <CInputGroupText>Name</CInputGroupText>
            <CFormInput
              type="text"
              value={editingProduct.name}
              onChange={(e) =>
                setEditingProduct({ ...editingProduct, name: e.target.value })
              }
            />
          </CInputGroup>
          <CInputGroup className="mb-3">
            <CInputGroupText>Package Price</CInputGroupText>
            <CFormInput
              type="number"
              step="0.01"
              value={editingProduct.package_price}
              onChange={(e) =>
                setEditingProduct({
                  ...editingProduct,
                  package_price: parseFloat(e.target.value),
                })
              }
            />
          </CInputGroup>
          <CInputGroup className="mb-3">
            <CInputGroupText>Package Currency/Selling Currency</CInputGroupText>
            <CFormInput
              type="text"
              value={editingProduct.package_currency}
              onChange={(e) =>
                setEditingProduct({
                  ...editingProduct,
                  package_currency: e.target.value,
                })
              }
            />
          </CInputGroup>
          <CInputGroup className="mb-3">
            <CInputGroupText>Selling Price </CInputGroupText>
            <CFormInput
              type="text"
              value={editingProduct.selling_price}
              onChange={(e) =>
                setEditingProduct({
                  ...editingProduct,
                  selling_price: e.target.value,
                })
              }
            />
          </CInputGroup>
          <CInputGroup className="mb-3">
            <CInputGroupText>Selling Weight </CInputGroupText>
            <CFormInput
              type="text"
              value={editingProduct.selling_weight}
              onChange={(e) =>
                setEditingProduct({
                  ...editingProduct,
                  selling_weight: e.target.value,
                })
              }
            />
          </CInputGroup>
          <CInputGroup className="mb-3">
            <CInputGroupText>Selling Weight Measurement </CInputGroupText>
            <CFormInput
              type="text"
              value={editingProduct.selling_weight_measurement}
              onChange={(e) =>
                setEditingProduct({
                  ...editingProduct,
                  selling_weight_measurement: e.target.value,
                })
              }
            />
          </CInputGroup>
          <CInputGroup className="mb-3">
            <CInputGroupText>Package Description</CInputGroupText>
            <CFormTextarea
              value={editingProduct.package_description}
              onChange={(e) =>
                setEditingProduct({
                  ...editingProduct,
                  package_description: e.target.value,
                })
              }
            />
          </CInputGroup>
          <CInputGroup className="mb-3">
            <CInputGroupText>Country </CInputGroupText>
            <CFormInput
              type="text"
              value={editingProduct.country}
              onChange={(e) =>
                setEditingProduct({
                  ...editingProduct,
                  country: e.target.value,
                })
              }
            />
          </CInputGroup>
          <CInputGroup className="mb-3">
          <CInputGroupText>City </CInputGroupText>
            <CFormInput
              type="text"
              value={editingProduct.city}
              onChange={(e) =>
                setEditingProduct({
                  ...editingProduct,
                  city: e.target.value,
                })
              }
            />
          </CInputGroup>
          <CInputGroup className="mb-3">
            <CInputGroupText>District</CInputGroupText>
            <CFormInput
              type="text"
              value={editingProduct.district}
              onChange={(e) =>
                setEditingProduct({
                  ...editingProduct,
                  district: e.target.value,
                })
              }
            />
          </CInputGroup>      
            <CInputGroup className="mb-3">
            <CFormInput
                type="file"
                id="formFile"
                label=""
                onChange={(e) => {
                const imageFile = e.target.files[0];
                setEditingProduct({ ...editingProduct, imageFile });
                }}
            />
            </CInputGroup>

          <CButton color="success" onClick={saveEditedProduct}>
            Save
          </CButton>
          <CButton color="secondary" onClick={cancelEdit}>
            Cancel
          </CButton>
        </form>
      </CCardBody>
    </CCard>
  </CCollapse>
)}
       
    </>
  )
}

export default ProductTable
