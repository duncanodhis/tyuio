import React from 'react'
import { CFooter } from '@coreui/react'

const AppFooter = () => {
  return (
    <CFooter>
      <div>
        <a href="https://" target="_blank" rel="noopener noreferrer">
          AdminHub
        </a>
        <span className="ms-1">&copy; 2023 adminHubLabs.</span>
      </div>
      <div className="ms-auto">
        <span className="me-1">Powered by</span>
        <a href="https://" target="_blank" rel="noopener noreferrer">
          AdminHubLabs
        </a>
      </div>
    </CFooter>
  )
}

export default React.memo(AppFooter)
