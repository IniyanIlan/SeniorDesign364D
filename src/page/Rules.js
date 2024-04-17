import React from 'react';
import { useNavigate } from "react-router";

// Import your JPEG images
import page1 from './images/page1.jpg';
import page2 from './images/page2.jpg';
import page3 from './images/page3.jpg';
import page4 from './images/page4.jpg';
import page5 from './images/page5.jpg';
import page6 from './images/page6.jpg';
import page7 from './images/page7.jpg';
import page8 from './images/page8.jpg';
import page9 from './images/page9.jpg';
import page10 from './images/page10.jpg';

// Add imports for other JPEG images as needed

const Rules = () => {
  const navigate = useNavigate();
  const handleBackHome = () => {
    // Add any logout logic here if needed
    navigate('/');
  }

  return (
    <div>
      <h2>Game Rules</h2>
      {/* <button style={{position: 'absolute', top: '10px', right: '10px', width: '100px'}} onClick={handleBackHome}>Back Home</button> */}
      <button className="button-top-left" onClick={handleBackHome}>Back Home</button>
      <div className="pdf-container">
        {/* Render each JPEG image as a page */}
        <img src={page1} alt="Page 1" className="pdf-page" />
        <img src={page2} alt="Page 2" className="pdf-page" />
        <img src={page3} alt="Page 3" className="pdf-page" />
        <img src={page4} alt="Page 4" className="pdf-page" />
        <img src={page5} alt="Page 5" className="pdf-page" />
        <img src={page6} alt="Page 6" className="pdf-page" />
        <img src={page7} alt="Page 7" className="pdf-page" />
        <img src={page8} alt="Page 8" className="pdf-page" />
        <img src={page9} alt="Page 9" className="pdf-page" />
        <img src={page10} alt="Page 10" className="pdf-page" />
        {/* Add more <img> elements for additional pages */}
      </div>
    </div>
  );
};

export default Rules;









// import React from 'react';
// import { Document, Page, pdfjs } from 'react-pdf';
// import { Link } from 'react-router-dom';
// // import gameRulesPdf from './game_rules.pdf';
// import gameRulesPdf from './Rulebook.pdf';

// pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

// const Rules = () => {
//   const onDocumentLoadSuccess = ({ numPages }) => {
//     console.log('Document loaded:', numPages);
//   };

//   return (
//     <div>
//       <h2>Game Rules</h2>
//       <Document file={gameRulesPdf} onLoadSuccess={onDocumentLoadSuccess}>
//         {Array.from(new Array(10), (el, index) => (
//           <Page key={`page_${index + 1}`} pageNumber={index + 1} />
//         ))}
//       </Document>
//       <Link to="/">Go back to Home</Link>
//     </div>
//   );
// };

// export default Rules;