function handlevote(can_name) {
    console.log(can_name);
    if (can_name != "Vote registered"){

        fetch(`${window.origin}/vote`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              can_name: can_name,
            }),
          }).then((resp) => {
              console.log(resp);
              window.location.reload();

            });
        
    }
}