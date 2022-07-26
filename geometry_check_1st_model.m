% Launch Motor-CAD
mcad = actxserver('MotorCAD.AppAutomation');

file_path='D:\KDH\Thesis\HDEV\02_MotorCAD\'
mot_file_name='12P72S_N42EH_Maxis_Force.mot'
file_name=strcat(file_path,mot_file_name);
% load from file
invoke(mcad,'LoadFromFile',file_name);

%% 1. Getvariable information current MCAD Mot file variable (#426)

% parameter_txt='D:\KDH\Thesis\HDEV\02_MotorCAD\ActiveXParameters_dimension.txt'
% parameter_mat=readtable(parameter_txt)
% use mcad ActiveX_parameters - find function is easy to use

% Toggle option


% radial

% axial

% *******************************************


%% Radial Dimensions
% Housing
[success,mcad_geometry.Housing.Housing_Dia] = invoke(mcad,'GetVariable','Housing_Dia');
[success,mcad_geometry.Housing.Housing_Add_F] = invoke(mcad,'GetVariable','StepHouseInner_F');
[success,mcad_geometry.Housing.Housing_Add_R] = invoke(mcad,'GetVariable','StepHouseInner_R');

% Stator
[success,mcad_geometry.stator.Stator_Lam_Dia] = invoke(mcad,'GetVariable','Stator_Lam_Dia');
[success,mcad_geometry.stator.Stator_Bore] = invoke(mcad,'GetVariable','Stator_Bore');

[success,mcad_geometry.Airgap] = invoke(mcad,'GetVariable','Airgap');

% Banding
[success,mcad_geometry.Banding_Thickness] = invoke(mcad,'GetVariable','Airgap');

% Sleeve
[success,mcad_geometry.Sleeve_Thickness] = invoke(mcad,'GetVariable','Airgap');

% Wafter
[success,mcad_geometry.Wafter_Number_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Wafter_Number_R] = invoke(mcad,'GetVariable','Airgap');

% shaft
[success,mcad_geometry.Shaft.Dia] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Shaft.Dia_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Shaft.Dia_R] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Shaft.Hole_Dia] = invoke(mcad,'GetVariable','Airgap');

% Winding

% EndWinding
[success,mcad_geometry.stator.Winding.EndWinding.add_outer_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.stator.Winding.Winding.EndWinding.add_outer_R] = invoke(mcad,'GetVariable','Airgap');

[success,mcad_geometry.stator.Winding.EndWinding.add_inner_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.stator.Winding.EndWinding.add_inner_R] = invoke(mcad,'GetVariable','Airgap');

[success,mcad_geometry.stator.Winding.EndWinding.Insulation_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.stator.Winding.EndWinding.Insulation_R] = invoke(mcad,'GetVariable','Airgap');

% Bearing
[success,mcad_geometry.Bearing.Dia_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Bearing.Dia_R] = invoke(mcad,'GetVariable','Airgap');

% Enconder
[success,mcad_geometry.Encoder.Shaft_dia] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Encoder.Case_dia] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Encoder.Case_Thick] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Encoder.Radial_gap] = invoke(mcad,'GetVariable','Airgap');

% Housing Cover
% water jacket axial
[success,mcad_geometry.Housing.Fin_Base_Thickness] = invoke(mcad,'GetVariable','StepHouseInner_R');
[success,mcad_geometry.Housing.Fin_Cover_Thickness] = invoke(mcad,'GetVariable','StepHouseInner_R');

% *******************************************


% % Axial Dimensions
% Housing
[success,mcad_geometry.Housing.Motor_Length] = invoke(mcad,'GetVariable','Airgap');   % ***Endcap including length
% Stator
[success,mcad_geometry.stator.Stator_Lam_Length] = invoke(mcad,'GetVariable','Airgap');
% magnet
[success,mcad_geometry.rotor.magnet.axial_length] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.rotor.magnet.axial_segment] = invoke(mcad,'GetVariable','Airgap');
% Rotor
[success,mcad_geometry.rotor.axial_length] = invoke(mcad,'GetVariable','Airgap');
% Stator
[success,mcad_geometry.stator.Stator_Axial_Offset] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.rotor.magnet.Magnet_Axial_Offset] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.rotor.Rotor_Axial_Offset] = invoke(mcad,'GetVariable','Airgap');
% Winding 
[success,mcad_geometry.stator.Winding.EndWinding.overhang_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.stator.Winding.EndWinding.overhang_R] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.stator.Winding.EndWinding.Axial_Extension_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.stator.Winding.EndWinding.Axial_Extension_R] = invoke(mcad,'GetVariable','Airgap');

% Housing 
% EndCap
[success,mcad_geometry.Housing.Endcap.Endcap_Length_F] = invoke(mcad,'GetVariable','StepHouseInner_R');
[success,mcad_geometry.Housing.Endcap.Endcap_Length_R] = invoke(mcad,'GetVariable','StepHouseInner_R');
[success,mcad_geometry.Housing.Endcap.Endcap_Thickness_F] = invoke(mcad,'GetVariable','StepHouseInner_R');
[success,mcad_geometry.Housing.Endcap.Endcap_Thickness_R] = invoke(mcad,'GetVariable','StepHouseInner_R');

% shaft
[success,mcad_geometry.Housing.Endcap.Shaft_Extension_F] = invoke(mcad,'GetVariable','StepHouseInner_R');
[success,mcad_geometry.Housing.Endcap.Shaft_Extension_R] = invoke(mcad,'GetVariable','StepHouseInner_R');

% Bearing
[success,mcad_geometry.Bearing.Bearing_Width_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Bearing.Bearing_Width_R] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Bearing.Bearing_axial_offset_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Bearing.Bearing_axial_offset_R] = invoke(mcad,'GetVariable','Airgap');

% Plate
    % Stator

[success,mcad_geometry.stator.Stator_Plate_Thick_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.stator.Stator_Plate_Thick_R] = invoke(mcad,'GetVariable','Airgap');
    % rotor
[success,mcad_geometry.rotor.Rotor_Plate_Thick_F] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.rotor.Rotor_Plate_Thick_R] = invoke(mcad,'GetVariable','Airgap');

% Feedback Encoder
[success,mcad_geometry.Encoder.Enc_Length] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Encoder.Enc_Case_Length] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Encoder.Enc_Barrier_Length] = invoke(mcad,'GetVariable','Airgap');
[success,mcad_geometry.Encoder.Enc_Axial_Gap] = invoke(mcad,'GetVariable','Airgap');

%% 1.1 Getmass
[success,mcad_geometry.total_weight] = invoke(mcad,'GetVariable','Weight_Total');
measure.total_weight=254;


% Housing
[success,mcad_geometry.Housing.Weight_Total_Housing_Total] = invoke(mcad,'GetVariable','Weight_Total_Housing_Total');
measure.Housing.Weight_Total_Housing_Total=51.53;



% End cover
[success,mcad_geometry.Housing.Endcap.Weight_Total_Endcap_Front] = invoke(mcad,'GetVariable','Weight_Total_Endcap_Front');
[success,mcad_geometry.Housing.Endcap.Weight_Total_Endcap_Rear] = invoke(mcad,'GetVariable','Weight_Total_Endcap_Rear');

measure.Housing.Endcap.Weight_Total_Endcap_Front=36.58;
measure.Housing.Endcap.Weight_Total_Endcap_Rear=28.75;





% stator
[success,mcad_geometry.stator.Weight_Total_Stator_Lam] = invoke(mcad,'GetVariable','Weight_Total_Stator_Lam');
measure.stator.Weight_Total_Stator_Lam=44;


[success,mcad_geometry.stator.Weight_Total_Stator_Lam_Back_Iron] = invoke(mcad,'GetVariable','Weight_Total_Stator_Lam_Back_Iron');
[success,mcad_geometry.stator.Weight_Total_Stator_Lam_Tooth] = invoke(mcad,'GetVariable','Weight_Total_Stator_Lam_Tooth');



% stator.winding
[success,mcad_geometry.stator.winding.Weight_Total_Armature_Copper_Total] = invoke(mcad,'GetVariable','Weight_Total_Armature_Copper_Total');

measure.stator.winding.Weight_Total_Armature_Copper_Total=21.5;

% stator.winding.end

% rotor

% rotor core
[success,mcad_geometry.rotor.Weight_Total_Rotor_Lam] = invoke(mcad,'GetVariable','Weight_Total_Rotor_Lam');

measure.rotor.Weight_Total_Rotor_Lam=0;

% rotor magnet
[success,mcad_geometry.rotor.magnet.Weight_Total_Magnet] = invoke(mcad,'GetVariable','Weight_Total_Magnet');

mcad_geometry.rotor.Weight_Total_Magnet =mcad_geometry.rotor.magnet.Weight_Total_Magnet;
measure.rotor.magnet.Weight_Total_Magnet=0;
measure.rotor.Weight_Total_Magnet=measure.rotor.magnet.Weight_Total_Magnet;

% Bearing

% shaft


% 
% *******************************************

%% 2. Setvariable allocate material properties
% matlab scdm coupling 
% check python
% check SCDM API


% % 3. Import dxf geometry 
% % 3.1 Import measurement mass


% % calculate geometry difference

% %  3.2 change mcad geometry





%% 3. Import DXF  dxf geometry
% % active
% dxf
% dxf_geometry.stator.winding.end=struct()
% dxf_geometry.stator.winding.end
% 
% dxf_geometry.stator.winding.active_length=146
% dxf_geometry.stator.active_length=241
% dxf_geometry.stator.outer_radius=440
% dxf_geometry.stator.inner_radius=400
% 
% % mcad
% mcad_geometry.stator.winding.active_length=146
% mcad_geometry.stator.winding.diff_Lst_LactiveW=16
% mcad_geometry.axial.Motor_length=struct();
% % mcad_geometry.axial.Motor_length.value=
% 
% % % front
% 
% % dxf
% dxf_geometry.stator.winding.end.frontlength=32
% dxf_geometry.stator.winding.end.front2stator=58;
% dxf_geometry.stator.winding.end.front_straight2stator=17;
% dxf_geometry.stator.winding.end.front2stator=45;
% dxf_geometry.stator.winding.end.front_straight2stator=8;
% % dxf_geometry.stator.winding.end.frontlength
% dxf_geometry.stator.winding.end.frontlength=37
% 
% % mcad
% mcad_geometry.stator=struct()
% mcad_geometry.stator.winding=struct()
% mcad_geometry.stator.winding.end=[]
% mcad_geometry.stator.winding.end=struct()
% mcad_geometry.stator.winding.end.frontlengh=[]
% 
% % %  rear
% % % dxf
% dxf_geometry.stator.winding.end.rearlength=32;
% dxf_geometry.stator.winding.end.rear2stator=58;
% dxf_geometry.stator.winding.end.rear_straight2stator=17;
% dxf_geometry.stator.winding.end.rear_straight2stator=8;
% dxf_geometry.stator.winding.end.rearlength
% dxf_geometry.stator.winding.end.rearlength=47
% 
% % mcad
% 
% 






%% 4.  calculate mass difference

diff_mass.total_weight= mcad_geometry.total_weight - measure.total_weight;
diff_mass.Housing.Weight_Total_Housing_Total = mcad_geometry.Housing.Weight_Total_Housing_Total - measure.Housing.Weight_Total_Housing_Total;
diff_mass.Housing.Endcap.Weight_Total_Endcap_Front= mcad_geometry.Housing.Endcap.Weight_Total_Endcap_Front - measure.Housing.Endcap.Weight_Total_Endcap_Front;
diff_mass.Housing.Endcap.Weight_Total_Endcap_Rear= mcad_geometry.Housing.Endcap.Weight_Total_Endcap_Rear - measure.Housing.Endcap.Weight_Total_Endcap_Rear;
diff_mass.stator.Weight_Total_Stator_Lam = mcad_geometry.stator.Weight_Total_Stator_Lam - measure.stator.Weight_Total_Stator_Lam;
diff_mass.stator.winding.Weight_Total_Armature_Copper_Total = mcad_geometry.stator.winding.Weight_Total_Armature_Copper_Total - measure.stator.winding.Weight_Total_Armature_Copper_Total;



% % 4. Setvariable

% % 
% [success,mcad_geometry.Housing.calib.Weight_Addition_Housing_Active] = invoke(mcad,'GetVariable','Weight_Addition_Housing_Active');
% [success,mcad_geometry.Housing.calib.Weight_Addition_Housing_Front] = invoke(mcad,'GetVariable','Weight_Addition_Housing_Front');
% [success,mcad_geometry.Housing.calib.Weight_Addition_Housing_Rear] = invoke(mcad,'GetVariable','Weight_Addition_Housing_Rear');

% [success,mcad_geometry.Housing.Endcap.calib.Weight_Addition_Endcap_Front] = invoke(mcad,'GetVariable','Weight_Addition_Endcap_Front');
% [success,mcad_geometry.Housing.Endcap.calib.Weight_Addition_Endcap_Rear] = invoke(mcad,'GetVariable','Weight_Addition_Endcap_Rear');

% 현재 데이터 불러와서 넣기
Weight_Addition_Housing_Active = mcad_geometry.Housing.calib.Weight_Addition_Housing_Active;
Weight_Addition_Housing_Front = mcad_geometry.Housing.calib.Weight_Addition_Housing_Front;
Weight_Addition_Housing_Rear = mcad_geometry.Housing.calib.Weight_Addition_Housing_Rear;
Weight_Addition_Endcap_Front = mcad_geometry.Housing.Endcap.calib.Weight_Addition_Endcap_Front;
Weight_Addition_Endcap_Rear = mcad_geometry.Housing.Endcap.calib.Weight_Addition_Endcap_Rear;

% % 4.1 Set weight addition

% manual하게 설정시 활성화할것
% Weight_Addition_Housing_Active = 0;
% Weight_Addition_Housing_Front = 0;
% Weight_Addition_Housing_Rear = 0;
% Weight_Addition_Endcap_Front = 0;
% Weight_Addition_Endcap_Rear = 0;

invoke(mcad,'SetVariable','Weight_Addition_Housing_Active', Weight_Addition_Housing_Active);
invoke(mcad,'SetVariable','Weight_Addition_Housing_Front', Weight_Addition_Housing_Front);

invoke(mcad,'SetVariable','Weight_Addition_Housing_Rear', Weight_Addition_Housing_Rear);
invoke(mcad,'SetVariable','Weight_Addition_Endcap_Front', Weight_Addition_Endcap_Front);

invoke(mcad,'SetVariable','Weight_Addition_Endcap_Rear', Weight_Addition_Endcap_Rear);


% 5 Get Mode 
