const nodemailer =  require('nodemailer');




const sendVerificationEmail = async (email, userID) => {
    const transporter = nodemailer.createTransport({
        service: 'gmail', 
        host: "smtp@gmail.com",
        port: 587,
        secure: false,
        auth : {
            user: 'jaundicedindividual@gmail.com',
            pass: 'ocdvalfeifeglckz'
        },
    });


    const verificationUrl = `http://localhost:8000/verify/${userID}`;


    const mailOptions = {
        from: 'jaundicedindividual@gmail.com',
        to: email,
        subject: 'HOF SPORTS: Verify Email',
        html: `<html>
                    <body>
                <p>Please verify your email by clicking the link below:</p>
                <a href = "${verificationUrl}">Verify Email </a>
                     </body>
                </html>`,
    };


    await transporter.sendMail(mailOptions);

    console.log("Debug: --sendVerificationEmail-- Email has been sent")
};

module.exports = sendVerificationEmail;