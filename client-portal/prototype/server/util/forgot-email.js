const nodemailer =  require('nodemailer');



const sendForgotEmail = async (email, password) => {

    console.log("Okay, I'm in the sendForgotEmail function");

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

    console.log("Transport created")



    const mailOptions = {
        from: 'jaundicedindividual@gmail.com',
        to: email,
        subject: 'HOF SPORTS: Forgot Password',
        html: `<html>
                    <body>
                <p>Here is your password:</p>
                <p>${password}</p>
                     </body>
                </html>`,
    };


    await transporter.sendMail(mailOptions);

    console.log("DEBUG: --sendForgotEmail-- Email has been sent")
};

module.exports = sendForgotEmail;