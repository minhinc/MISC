<?php
if(isset($_FILES["photo"]["error"])){
    if($_FILES["photo"]["error"] > 0){
        echo "Error: " . $_FILES["photo"]["error"] . "<br>";
    } else{
        $allowed = array("pdf" => "application/pdf",  "docx" => "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "txt" => "text/plain", "jpg" => "image/jpg", "jpeg" => "image/jpeg", "gif" => "image/gif", "png" => "image/png" );
        //$allowed = array("jpg" => "image/jpg", "jpeg" => "image/jpeg", "gif" => "image/gif", "png" => "image/png", "pdf" => "application/pdf", "doc" => "application/msword", "docx" => "application/msword", "txt" => "text/plain");
        $filename = $_FILES["photo"]["name"];
        $filetype = $_FILES["photo"]["type"];
        $filesize = $_FILES["photo"]["size"];
//        echo "File Type: " . $_FILES["photo"]["type"] . "<br>";
    
        // Verify file extension
        $ext = pathinfo($filename, PATHINFO_EXTENSION);
        if(!array_key_exists($ext, $allowed)) die("<p style=\"color:#ff0000\">Error: Please select a valid file format.</p>");
    
        // Verify file size - 5MB maximum
//        $maxsize = 5 * 1024 * 1024;
        $maxsize = 900 * 1024;
        if($filesize > $maxsize) die("<p style=\"color:#ff0000\">Error: File size is larger than 900KB the allowed limit.</p>");
    
        // Verify MYME type of the file
        if(in_array($filetype, $allowed)){
            // Check whether file exists before uploading it
            if(file_exists("../career/upload/" . $_FILES["photo"]["name"])){
                echo "<p style=\"color:#004000\">" . $_FILES["photo"]["name"] . " already exists.</p>";
            } else{
                move_uploaded_file($_FILES["photo"]["tmp_name"], "../career/upload/" . $_FILES["photo"]["name"]);
                echo "<p style=\"color:#004000\">Your file was uploaded successfully.</p>";
                mail("sales@minhinc.com","Bio submission","","From:career@minhinc.com");
            } 
        } else{
            echo "<p style=\"color:#ff0000\">Error: There was a problem uploading your file - please try again.</p>"; 
        }
    }
} else{
    echo "<p style=\"color:#ff0000\">Error: Invalid parameters - please contact your server administrator.</p>";
}
?>
