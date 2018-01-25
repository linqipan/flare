<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
<!--    <title>file read and write test</title>-->
    <style>
        h3 {
            margin-left: 280px;
        }
        .image-display {
            /*margin:auto;*/
            margin-top: 100px;
            width: 784px;
            height:672px;
            background-size: 100% 100%;
        }
        .img-group {
            display: inline-block;
        }
        #Disp_vector {
            background: url("Disp_vector.png");
        }
        #Temp_plot {
            background: url("Temp_plot.png");
        }
        #Von_Mises {
            background: url("Von_Mises.png");
        }
        #ScreenMesh {
            background: url("ScreenMesh.png");
        }
    </style>
</head>
<body>

<?php

//========function to make directories to save image files==================
$DirNameArr = ['result'];
/*------------definition of function ------------*/
$DirNameArr = array_filter($DirNameArr); //filler
mkDirectory($DirNameArr); //calling the function to make directories
function mkDirectory($DirNameArr) {
    if (count($DirNameArr) != 0) {
        for ($i = 0; $i < count($DirNameArr); $i ++) {
            if (trim(($DirNameArr[$i])) != '' && !is_dir(trim(($DirNameArr[$i])))) {
                mkdir($DirNameArr[$i]);
            }
        }
    }
}
//=======end mkDirectory function calling===================

//=============Reading JSON file===================
$json_string = file_get_contents('myjson_P2.json');
$main_var = json_decode($json_string, true);
//=============Geometrical Parameter file for GMSH======
$f_head = '
 //Total_number; Total number of sections to be considered
 //lz; location in longitudinal direction of the sections
 //diameter; diameter of sections
 //el_num...; element number';
$fgeo = fopen('Product2_geo.par', 'w+' );
fwrite($fgeo,$f_head."\n\n\n");
fwrite($fgeo, 'inlet_dia = ' . $main_var['inlet_dia'] . ';'. "\n");
fwrite($fgeo, 'inlet_length = ' . $main_var['inlet_length'] . ';'. "\n");
fwrite($fgeo, 'nozzle_dia = ' . $main_var['nozzle_dia'] . ';'. "\n");
fwrite($fgeo, 'nozzle_length = ' . $main_var['nozzle_length'] . ';'. "\n");
fwrite($fgeo, 'pad_width = ' . $main_var['pad_width'] . ';'. "\n");
fwrite($fgeo, 'el_size = ' . $main_var['el_size'] . ';'. "\n");
fclose($fgeo);

////========= Material and section file for ccx ===========
$fid_mat = fopen('material.inp', 'w+' );
fwrite($fid_mat, '*MATERIAL, NAME=inlet_material'."\n");
fwrite($fid_mat, '*ELASTIC' . "\n");
fwrite($fid_mat, $main_var['inlet_material']['young'] . ',' . $main_var['inlet_material']['nu'] . "\n");
fwrite($fid_mat, '*EXPANSION' . "\n");
fwrite($fid_mat, $main_var['inlet_material']['expansion']  . "\n");

fwrite($fid_mat, '*MATERIAL, NAME=nozzle_material'."\n");
fwrite($fid_mat, '*ELASTIC' . "\n");
fwrite($fid_mat, $main_var['nozzle_material']['young'] . ',' . $main_var['nozzle_material']['nu'] . "\n");
fwrite($fid_mat, '*EXPANSION' . "\n");
fwrite($fid_mat, $main_var['nozzle_material']['expansion']  . "\n");

fwrite($fid_mat, '*MATERIAL, NAME=pad_material'."\n");
fwrite($fid_mat, '*ELASTIC' . "\n");
fwrite($fid_mat, $main_var['pad_material']['young'] . ',' . $main_var['pad_material']['nu'] . "\n");
fwrite($fid_mat, '*EXPANSION' . "\n");
fwrite($fid_mat, $main_var['pad_material']['expansion']  . "\n");

fwrite($fid_mat, '*SHELL SECTION, ELSET=inlet, MATERIAL=inlet_material' . "\n");
fwrite($fid_mat, $main_var['inlet_thick']  . "\n");
fwrite($fid_mat, '*SHELL SECTION, ELSET=nozzle, MATERIAL=nozzle_material' . "\n");
fwrite($fid_mat, $main_var['nozzle_thick']  . "\n");
fwrite($fid_mat, '*SHELL SECTION, ELSET=pad, MATERIAL=pad_material' . "\n");
$pad_thick = $main_var['pad_thick'] + $main_var['inlet_thick'];
fwrite($fid_mat, $pad_thick  . "\n");
fwrite($fid_mat, '*NODE' . "\n");
fwrite($fid_mat, '1000001, 0, 0, '. ($main_var['inlet_length'] + 1) . "\n");
fwrite($fid_mat, '1000002, 0, 0, '. $main_var['inlet_length'] . "\n");
fwrite($fid_mat, '1000003, '. ($main_var['inlet_dia']/2 + $main_var['nozzle_length']) .', 0, '.($main_var['inlet_length']/2) ."\n");
fwrite($fid_mat, '1000004, '. ($main_var['inlet_dia']/2 + $main_var['nozzle_length']+1) .', 0, '.($main_var['inlet_length']/2) ."\n");
fwrite($fid_mat, '*rigid body, nset=inlet_end_2, ref node = 1000001 , rot node = 1000002' . "\n");
fwrite($fid_mat, '*rigid body, nset=nozzle_end, ref node = 1000003 , rot node = 1000004' . "\n");
fclose($fid_mat); // file close
//=========end writing Material file========

//=========writing load.inp file===========
$fid_load = fopen('load.inp', 'w+' );
fwrite($fid_load, '*TEMPERATURE' . "\n");
fwrite($fid_load, 'Nall, ' . $main_var['Temp'] . "\n");
fwrite($fid_load, '*CLOAD' . "\n");
fwrite($fid_load, '1000001, 1, '. $main_var['inlet_load']['Fx'] . "\n");
fwrite($fid_load, '1000001, 2, '. $main_var['inlet_load']['Fy'] . "\n");
fwrite($fid_load, '1000001, 3, '. $main_var['inlet_load']['Fz'] . "\n");

fwrite($fid_load, '1000002, 1, '. $main_var['inlet_load']['Mx'] . "\n");
fwrite($fid_load, '1000002, 2, '. $main_var['inlet_load']['My'] . "\n");
fwrite($fid_load, '1000002, 3, '. $main_var['inlet_load']['Mz'] . "\n");

fwrite($fid_load, '1000003, 1, '. $main_var['nozzle_load']['Fx'] . "\n");
fwrite($fid_load, '1000003, 2, '. $main_var['nozzle_load']['Fy'] . "\n");
fwrite($fid_load, '1000003, 3, '. $main_var['nozzle_load']['Fz'] . "\n");

fwrite($fid_load, '1000004, 1, '. $main_var['nozzle_load']['Mx'] . "\n");
fwrite($fid_load, '1000004, 2, '. $main_var['nozzle_load']['My'] . "\n");
fwrite($fid_load, '1000004, 3, '. $main_var['nozzle_load']['Mz'] . "\n");

//1000002,1,3.0000E+04
fclose($fid_load);
//=======end writing load file===========


//== running of GMSH ===========
$fid = fopen('Product2_gmsh.bat', 'w+' );
fwrite($fid, 'gmsh Product2.geo');
fclose($fid);
exec("Product2_gmsh.bat");
//== end of running of GMSH =========

//
//================INPUT file names==================
$Input_file_name = 'Product2_gmsh.inp';
$Output_file_name = 'Product2_ccxmsh.inp';

//
FileInOut($Input_file_name, $Output_file_name); // call to function FileInOut
//

//== running of CCX ===========
$fid = fopen('Product2_ccx.bat', 'w+' );
fwrite($fid, 'cmd /C "C:\Program Files (x86)\bConverged\common\site\cmdStartup.bat" ccx product2_ccx');
fclose($fid);
//
exec("Product2_ccx.bat");
//
//== running of CGX ===========
$fid = fopen('Product2_cgx.bat', 'w+' );
fwrite($fid, 'cmd /K "C:\Program Files (x86)\bConverged\common\site\cmdStartup.bat" cgx -b Product2_cgx_inp.fbd');
fclose($fid);

exec("Product2_cgx.bat");
//
//
?>
<?php //list($width, $height) = getimagesize("ScreenMesh.png");?>
<div class="img-group">
    <div id="ScreenMesh" class="image-display" >

<!--            <h1 style="color: #fb1561;">>>>> Mesh for product 1 </h1>-->
    </div>
    <h3>Finite Element Mesh</h3>
</div>
<div class="img-group">
    <div id="Temp_plot" class="image-display" >

        <!--    <h1 style="color: #fb1561;">>>>> Mesh for product 1 </h1>-->
    </div>
    <h3>Temperature Increment</h3>
</div>
<div class="img-group">
    <div id="Disp_vector" class="image-display" >

        <!--    <h1 style="color: #fb1561;">>>>> Mesh for product 1 </h1>-->
    </div>
    <h3>Displacement(mm)</h3>
</div>
<div class="img-group">
    <div id="Von_Mises" class="image-display" >
        <!--    <h1 style="color: #fb1561;">>>>> Mesh for product 1 </h1>-->
    </div>
    <h3>Von-mises stress(Mpa)</h3>
</div>
<?php
//=======copy specific file to specific position=================
$FileExtension = '*.png'; //specify file extension within directory to copy
$FileCopyPos = 'result/';

$copy_file = glob($FileExtension); // file name array of file extension to copy
copy_file($copy_file, $FileCopyPos);
/**
 * This function is the function to copy file to the specific directory
 * @param $filename_array
 * @param $FileCopyPos
 */
function copy_file($filename_array, $FileCopyPos) {
    if (count($filename_array) != 0) {
        for ($i = 0; $i < count($filename_array); $i ++) {
            copy($filename_array[$i], $FileCopyPos . $filename_array[$i]); // copy file name
        }
    }
}
//======end copy file=============================

//====== Converting mesh file of GMSH into CCX ======
////++++++++++++++++++++++++++++++++++++++++++++
FileInOut($Input_file_name, $Output_file_name); // call to function FileInOut
function FileInOut($Input_file_name, $Output_file_name)
{
    $lines = file($Input_file_name);//file to read
    $fid_w = fopen($Output_file_name, 'w+');
    $N = count($lines);

//=========finding star position ( Star means symbol "*")======
    $star = array();
    $star_lines = array();
    $j = 0;
    for ($i = 2; $i < $N; $i++) {
        if ($lines[$i][0] == '*') {
            $star[$j] = $i;
            $star_lines[$j] = $lines[$i];
            $j += 1;
        }
    }

//============Node=================
    $lines[2] = trim($lines[2]) . ', NSET=Nall' . "\n";
    fwrite($fid_w, $lines[2]);
    for ($iii = 0; $iii < count($star_lines); $iii++) {
        $line_explode = explode(',', $star_lines[$iii]);
        if (trim($line_explode[0]) == '*NODE') {
            for ($i = $star[$iii] + 1; $i < $star[$iii + 1]; $i++) {
                $node_temp = explode(',', $lines[$i]);
                $res_node = $node_temp[0];
                for ($k = 1; $k < count($node_temp); $k++) {
                    if(abs($node_temp[$k])<=1.0e-9) {
                        $node_temp[$k] = 0;
                    }
                    $res_node .= ',' . round($node_temp[$k], 12);
                }
                fwrite($fid_w, $res_node . "\n");
            }
            print_r($i);
        }
    }

//====************ELEMENT*************====
    $lines[$i] = '******* E L E M E N T S *************' . "\n";
    fwrite($fid_w, $lines[$i]);
//========Element CPS3=============
    $element_CPS3 = array();
    $lines[$i] = '*ELEMENT, TYPE=S3, ELSET=Shell' . "\n";
    fwrite($fid_w, $lines[$i]);
    for ($iii = 0; $iii < count($star_lines); $iii++) {
        $star_line_explode = explode(',', $star_lines[$iii]);
        if (trim($star_line_explode[0]) == '*ELEMENT') {
            if (trim($star_line_explode[1]) == 'type=CPS3') {
                for ($i = $star[$iii] + 1; $i < $star[$iii + 1]; $i++) {
                    $line_explode = explode(',', $lines[$i]);
                    $element_CPS3[$line_explode[0]] = $lines[$i];
                    fwrite($fid_w, $lines[$i]);
                }
            }
        }
    }
//========ELSET inlet=============
    for ($iii = 0; $iii < count($star_lines); $iii++) {
        $star_line_explode = explode(',', $star_lines[$iii]);
        if (trim($star_line_explode[0]) == '*ELSET') {
            if (trim($star_line_explode[1]) == 'ELSET=inlet') {
                for ($i = $star[$iii]; $i < $star[$iii + 1]; $i++) {
                    fwrite($fid_w, $lines[$i]);
                }
            }
        }
    }
//========ELSET nozzle=============
    for ($iii = 0; $iii < count($star_lines); $iii++) {
        $star_line_explode = explode(',', $star_lines[$iii]);
        if (trim($star_line_explode[0]) == '*ELSET') {
            if (trim($star_line_explode[1]) == 'ELSET=nozzle') {
                for ($i = $star[$iii]; $i < $star[$iii + 1]; $i++) {
                    fwrite($fid_w, $lines[$i]);
                }
            }
        }
    }
//========ELSET pad=============
    for ($iii = 0; $iii < count($star_lines); $iii++) {
        $star_line_explode = explode(',', $star_lines[$iii]);
        if (trim($star_line_explode[0]) == '*ELSET') {
            if (trim($star_line_explode[1]) == 'ELSET=pad') {
                for ($i = $star[$iii]; $i < $star[$iii + 1]; $i++) {
                    fwrite($fid_w, $lines[$i]);
                }
            }
        }
    }
//========NSET inlet_end_1=============
    for ($iii = 0; $iii < count($star_lines); $iii++) {
        $star_line_explode = explode(',', $star_lines[$iii]);
        if (trim($star_line_explode[0]) == '*NSET') {
            if (trim($star_line_explode[1]) == 'NSET=inlet_end_1') {
                for ($i = $star[$iii]; $i < $star[$iii + 1]; $i++) {
                    fwrite($fid_w, $lines[$i]);
                }
            }
        }
    }
//========NSET inlet_end_2=============
    for ($iii = 0; $iii < count($star_lines); $iii++) {
        $star_line_explode = explode(',', $star_lines[$iii]);
        if (trim($star_line_explode[0]) == '*NSET') {
            if (trim($star_line_explode[1]) == 'NSET=inlet_end_2') {
                for ($i = $star[$iii]; $i < $star[$iii + 1]; $i++) {
                    fwrite($fid_w, $lines[$i]);
                }
            }
        }
    }
//========NSET nozzle_end=============
    for ($iii = 0; $iii < count($star_lines); $iii++) {
        $star_line_explode = explode(',', $star_lines[$iii]);
        if (trim($star_line_explode[0]) == '*NSET') {
            if (trim($star_line_explode[1]) == 'NSET=nozzle_end') {
                for ($i = $star[$iii]; $i < $star[$iii + 1]; $i++) {
                    fwrite($fid_w, $lines[$i]);
                }
            }
        }
    }

    fclose($fid_w);

}//End FileInOut function

?>

</body>
</html>
