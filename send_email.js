require('dotenv').config();
const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER,  // Use .env variables
        pass: process.env.EMAIL_PASS
    }
});

// Function to send OTP email
function sendOTP(email, otp) {
    const mailOptions = {
        from: process.env.EMAIL_USER,
        to: email,
        subject: 'Your OTP Code',
        text: `Your OTP for verification is: ${otp}`
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.log("❌ Email Error:", error);
        } else {
            console.log("Email Sent:", info.response);
        }
    });
}

// Export function for Django to call
module.exports = { sendOTP };

// Test by running: node send_email.js email@example.com 123456
if (require.main === module) {
    const email = process.argv[2];  // Get email from command-line
    const otp = process.argv[3];  // Get OTP from command-line
    sendOTP(email, otp);
}
