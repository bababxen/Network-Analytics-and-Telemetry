const executeButton =
    document.getElementById("executeButton");

const routerIp =
    document.getElementById("routerIp");

const command =
    document.getElementById("command");

const output =
    document.getElementById("output");

const status =
    document.getElementById("status");


executeButton.addEventListener(
    "click",
    async function () {

        const ip =
            routerIp.value.trim();

        const cmd =
            command.value.trim();


        // Check input

        if (!ip) {

            output.textContent =
                "Please enter Router IP Address.";

            return;
        }


        if (!cmd) {

            output.textContent =
                "Please enter Router Command.";

            return;
        }


        // Disable button

        executeButton.disabled = true;

        executeButton.textContent =
            "Connecting...";

        status.textContent =
            "Connecting";


        output.textContent =
            "Connecting to router...\n";


        try {

            // Send request to Flask backend

            const response =
                await fetch(
                    "/api/execute",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            router_ip: ip,

                            command: cmd

                        })

                    }
                );


            const data =
                await response.json();


            // Successful

            if (data.success) {

                output.textContent =
                    data.output;

                status.textContent =
                    "Success";

            }


            // Error from backend

            else {

                output.textContent =
                    "ERROR\n\n" +
                    data.error;

                status.textContent =
                    "Error";

            }


        }


        catch (error) {

            output.textContent =
                "Cannot connect to backend.\n\n" +
                error;

            status.textContent =
                "Connection Error";

        }


        finally {

            executeButton.disabled =
                false;

            executeButton.textContent =
                "Execute Command";

        }

    }
);
