package com.example.mallesh.sensor_record;

import android.Manifest;
import android.app.Activity;
import android.app.ListActivity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.util.Log;
import android.widget.ArrayAdapter;

import org.influxdb.BatchOptions;
import org.influxdb.InfluxDB;
import org.influxdb.InfluxDBFactory;
import org.influxdb.dto.Point;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;
import javax.net.ssl.*;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends ListActivity implements SensorEventListener {
    //global variables
    public static final String file = ("data.txt");
    public static File myData = null;
    public static  File myDataCollection = null;
    public static final String DATA_COLLECTION_FILE = ("DataCollection.txt");
    public SensorEventListener mSensorListener ;
    public SensorManager sensorManager;
    public List<Sensor> listSensor;
    private  Sensor mAccelerometer,mProximity, mAmbientTemp, mGameRotationVect, mGeomagneticRotationVecor, mGravity, mGyroscope,
            mGyroUncal, mLight, mLinearAcceleration, mMagFld, mMagFldUncal, mOrientation, mPressure, mRelativeHumid, mRotVect,
            mSignificantMotion, mStepCntr, mStepDetect, mTemp;

    // Storage Permissions
    private static final int REQUEST_EXTERNAL_STORAGE = 1;
    private static String[] PERMISSIONS_STORAGE = {
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
    };

    /**
     * Checks if the app has permission to write to device storage
     *
     * If the app does not has permission then the user will be prompted to grant permissions
     *
     * @param activity
     */
    public static void verifyStoragePermissions(Activity activity) {
        // Check if we have write permission
        int permission = ActivityCompat.checkSelfPermission(activity, Manifest.permission.WRITE_EXTERNAL_STORAGE);

        if (permission != PackageManager.PERMISSION_GRANTED) {
            // We don't have permission so prompt the user
            ActivityCompat.requestPermissions(
                    activity,
                    PERMISSIONS_STORAGE,
                    REQUEST_EXTERNAL_STORAGE
            );
        }
    }

    private final static String INFLUX_HOST = "https://influx-cewit.netsmartdev.com:443";
    private static String INFLUX_DATABASE = "db_team_69";
    private static String INFLUX_USER = "user_team_69";
    private static String INFLUX_PASS = "J9sdscUlGImEzBEP";

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //creating Folder on device

        //String newFolder = "/myFolder2";
        //String extStorageDirectory = Environment.getExternalStorageDirectory().getPath().toString();
        //File myNewFolder = new File(extStorageDirectory + newFolder);
        //myNewFolder.mkdir();

        //myData = new File(extStorageDirectory + newFolder + "/"+ file);
        myData = new File("/sdcard/"+file);
        try{
            if(!myData.exists()){
                myData.createNewFile();
            }
        }catch(IOException ioExp){
            Log.d("AndroidSensorList::", "error in file creation");
        }

        //myDataCollection = new File(extStorageDirectory + newFolder + "/"+ DATA_COLLECTION_FILE);
        myDataCollection = new File("/sdcard/"+DATA_COLLECTION_FILE);
        try{
            if(!myDataCollection.exists()){
                myDataCollection.createNewFile();
            }
        }catch(IOException ioExp){
            Log.d("AndroidSensorList::", "error in file creation");
        }

        //retrieving the list of sensors available on a device
        sensorManager
                = (SensorManager)getSystemService(Context.SENSOR_SERVICE);
        listSensor
                = sensorManager.getSensorList(Sensor.TYPE_ALL);
        mAccelerometer=sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
//        mAmbientTemp=sensorManager.getDefaultSensor(Sensor.TYPE_AMBIENT_TEMPERATURE);
//        mGameRotationVect=sensorManager.getDefaultSensor(Sensor.TYPE_GAME_ROTATION_VECTOR);
//        mGeomagneticRotationVecor=sensorManager.getDefaultSensor(Sensor.TYPE_GEOMAGNETIC_ROTATION_VECTOR);
//        mGravity=sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY);
//        mGyroscope=sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
//        mGyroUncal=sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE_UNCALIBRATED);
//        mLight=sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);
//        mLinearAcceleration=sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
//        mMagFld=sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
//        mMagFldUncal=sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD_UNCALIBRATED);
//        mOrientation=sensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION);
//        mPressure=sensorManager.getDefaultSensor(Sensor.TYPE_PRESSURE);
//        mProximity=sensorManager.getDefaultSensor(Sensor.TYPE_PROXIMITY);
//        mRelativeHumid=sensorManager.getDefaultSensor(Sensor.TYPE_RELATIVE_HUMIDITY);
//        mRotVect=sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);
//        mSignificantMotion=sensorManager.getDefaultSensor(Sensor.TYPE_SIGNIFICANT_MOTION);
//        mStepCntr=sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER);
//        mStepDetect=sensorManager.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR);

        //Creating List view and writing data to a file

        List<String> listSensorType = new ArrayList<String>();
        for(int i=0; i<listSensor.size(); i++){
            System.out.println("Inside list sensors:::::::");
            listSensorType.add((i+1)+" "+listSensor.get(i).getName());
            String sensorNames = listSensor.get(i).getName();
            System.out.println(listSensor.get(i).getType());
            //mSensorManager.registerListener(mSensorListener, mSensorManager.getDefaultSensor(listSensor.get(i).getType()), SensorManager.SENSOR_DELAY_NORMAL);
            writeToFile(listSensor.get(i).getName().getBytes(),sensorNames );

        }

        setListAdapter(new ArrayAdapter<String>(this,
                android.R.layout.simple_list_item_1,
                listSensorType));
        getListView().setTextFilterEnabled(true);


        Thread thread = new Thread(new Runnable() {

            @Override
            public void run() {
                try {
                    System.out.println("Sending");
                    insertDataPoints(INFLUX_DATABASE, INFLUX_USER, INFLUX_PASS);
                } catch (Exception e) {
                    System.out.println("Caught");
                }
            }
        });

        thread.start();

    }


    private void writeToFile(byte[] data, String sensorNames) {
        System.out.println("----------------Inside writeToFile-----------------");

        try {
            String comma = "\n";
            byte[] bComma = comma.getBytes();
            OutputStream fo = new FileOutputStream(myData,true);
            fo.write(bComma);
            fo.write(data);
            fo.close();

        }
        catch (IOException e) {
            Log.e("AndroidSensorList::","File write failed: " + e.toString());
        }

    }


    protected void onResume() {
        super.onResume();
        sensorManager.registerListener(this,mAccelerometer,  SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mProximity, SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this,mAmbientTemp,  SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mGameRotationVect, SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this,mGeomagneticRotationVecor,  SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mGravity,  SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mGyroscope, SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mGyroUncal, SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mLight,  SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mLinearAcceleration, SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this,mMagFld,  SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this,mMagFldUncal,  SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this,mOrientation,   SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this,mPressure,   SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mRelativeHumid, SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this,mRotVect,  SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mSignificantMotion, SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this,mStepCntr,   SensorManager.SENSOR_DELAY_NORMAL);
//        sensorManager.registerListener(this, mStepDetect, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    protected void onPause() {
        sensorManager.unregisterListener(mSensorListener);
        super.onPause();

    }





    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // TODO Auto-generated method stub

    }

    private static void insertDataPoints(String database, String user, String password) throws InterruptedException {

        try {
            final TrustManager[] trustAllCerts = new TrustManager[]{
                    new X509TrustManager() {
                        @Override
                        public void checkClientTrusted(java.security.cert.X509Certificate[] chain, String authType) {
                        }

                        @Override
                        public void checkServerTrusted(java.security.cert.X509Certificate[] chain, String authType) {
                        }

                        @Override
                        public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                            return new java.security.cert.X509Certificate[]{};
                        }
                    }
            };

            // Install the all-trusting trust manager
            final SSLContext sslContext = SSLContext.getInstance("SSL");
            sslContext.init(null, trustAllCerts, new java.security.SecureRandom());
            // Create an ssl socket factory with our all-trusting manager
            final SSLSocketFactory sslSocketFactory = sslContext.getSocketFactory();

            OkHttpClient.Builder builder = new OkHttpClient.Builder();
            builder.sslSocketFactory(sslSocketFactory, (X509TrustManager) trustAllCerts[0]);
            builder.hostnameVerifier(new HostnameVerifier() {
                @Override
                public boolean verify(String hostname, SSLSession session) {
                    return true;
                }
            });
//        OkHttpClient.Builder builder = new OkHttpClient.Builder();
//        builder.hostnameVerifier(new HostnameVerifier() {
//            @Override
//            public boolean verify(String hostname, SSLSession session) {
//                return true;
//            }
//        });
            try (InfluxDB influxDB = InfluxDBFactory.connect(INFLUX_HOST, user, password, builder)) {

                // Set up exception handler
                influxDB.enableBatch(BatchOptions.DEFAULTS.exceptionHandler(
                        (failedPoints, throwable) -> {
                            for (Point failedPoint : failedPoints) {
                                System.err.println("[ERROR] Failed Point: " + failedPoint);
                            }
                            System.err.println(throwable);
                        })
                );

                // Set Database
                influxDB.setDatabase(database);

                // Create tags
                Map<String, String> tags = new HashMap<>();
    //            tags.put("component", "primary_web_app");
    //            tags.put("type", "method_timer");
    //            tags.put("user", System.getProperty("user.name"));
    //            tags.put("os", System.getProperty("os.name"));
    //            tags.put("hostname", InfluxDBInsert.getHostName());

                // Send 10 random metric values into the database
                for (int i = 0; i < 10; i++) {

                    // Random response time
    //                int responseTime = ThreadLocalRandom.current().nextInt(50, 10000);
    //
    //                // Random request size
    //                int payloadSize = ThreadLocalRandom.current().nextInt(1024, 10000);

                    // Create Point
                    Point point = Point.measurement("request_timer")
                            .time(System.currentTimeMillis(), TimeUnit.MILLISECONDS)
                            .tag(tags)
                            .addField("responseTimeMs", 10000)
                            .addField("requestSizeBytes", 2000)
                            .build();

                    // Write Point
                    influxDB.write(point);
                    System.out.println("[info] Wrote Point to Influx Db @ " + INFLUX_HOST + "/" + INFLUX_DATABASE);

                    Thread.sleep(2000);
                }
            }
        } catch (Exception e) {
            System.out.println("Something caught");
        }
    }



    @Override
    public final void onSensorChanged(SensorEvent event) {
        // TODO Auto-generated method stub
//        System.out.println("++++++++++++++++INSIDE onSensorChanged() ++++++++++++++++++++++");
        //System.out.println("sensorName:"+sensorName);
//        System.out.println("event.sensor.getName():"+event.sensor.getName());
        float x,y,z;

        x=event.values[0];
        y=event.values[1];
        z=event.values[2];
//        System.out.println(x);
//        System.out.println(y);
//        System.out.println(z);
        //writeDataTofile(event.sensor.getName(),x,y,z);

    }
    public void writeDataTofile(String sensorsName, float x, float y, float z){

        System.out.println(sensorsName+"::"+"X="+x+"Y="+y+"Z="+z);

        //mSensorManager.registerListener(mSensorListener, mSensorManager.getDefaultSensor(event.sensor.getType()), SensorManager.SENSOR_DELAY_NORMAL);
        String xVal= String.valueOf(x);
        String yVal= String.valueOf(y);
        String zVal= String.valueOf(z);
        byte[] bX_Value= xVal.getBytes();
        byte[] bY_Value= yVal.getBytes();
        byte[] bZ_Value= zVal.getBytes();
        String newLine = "\n";
        byte[] bnewLine = newLine.getBytes();
        String sSeparator="||";
        byte[] bSeparator=sSeparator.getBytes();
        byte[] bSensorName = sensorsName.getBytes();
        try{
            OutputStream fo = new FileOutputStream(myDataCollection,true);
            fo.write(bnewLine);
            fo.write(bSensorName);
            fo.write(bX_Value);
            fo.write(bSeparator);
            fo.write(bY_Value);
            fo.write(bSeparator);
            fo.write(bZ_Value);
            fo.write(bnewLine);
            fo.close();
        }catch(IOException e){
            Log.e("AndroidSensorList::","File write failed: " + e.toString());
        }
    }
}