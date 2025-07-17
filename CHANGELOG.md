# Changelog

All notable changes to the VOLVO MDC project will be documented in this file.

## [2.0.0] - 2025-07-17

### Added
- 📖 **DMC Code Reading Functionality**
  - Upload and decode DMC codes from images
  - Support for PNG, JPG, JPEG, GIF, BMP, TIFF formats
  - Real-time feedback and error handling
  - Integration with history system

- 🎨 **Enhanced User Interface**
  - Reorganized sections for generation and reading
  - Added visual indicators for operation types (🏭 Generate, 📖 Read)
  - Improved mobile responsiveness
  - Apple-inspired design consistency

- 📊 **Improved History System**
  - Distinguish between generated and read operations
  - Track source filenames for read operations
  - Enhanced visual representation

### Enhanced
- Updated README with comprehensive documentation
- Added API endpoint documentation
- Improved error handling and validation
- Enhanced mobile user experience

### Technical
- Added `read_dmc.py` module for DMC reading
- New `/read_dmc` API endpoint
- Enhanced JavaScript functionality
- Updated CSS styling for new features

## [1.0.0] - 2025-07-07

### Added
- 🏭 **DMC Code Generation**
  - Prefix selection (A-Z, 0-9)
  - Automatic timestamp-based code generation
  - Batch generation of 30 codes
  - 5x6 grid layout

- 📄 **Export Functions**
  - PDF export with VOLVO branding
  - Excel export in structured format
  - Print-optimized layouts

- 🔐 **Authentication System**
  - Secure login functionality
  - Session management

- 📱 **Responsive Design**
  - Mobile-first approach
  - Apple-inspired UI
  - Cross-platform compatibility

- 📊 **History Tracking**
  - JSON-based storage
  - Complete audit trail
  - Timestamp tracking

### Technical
- Flask backend architecture
- pylibdmtx integration
- FPDF and openpyxl support
- File-based database system

---

**Legend:**
- 🏭 Manufacturing/Generation features
- 📖 Reading/Decoding features  
- 🎨 UI/UX improvements
- 📊 Data/Analytics features
- 🔐 Security features
- 📱 Mobile features
- 📄 Export features
