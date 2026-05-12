package com.whatstats.app;

import android.content.ClipData;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.os.Parcelable;
import android.provider.OpenableColumns;
import com.getcapacitor.BridgeActivity;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Locale;

public class MainActivity extends BridgeActivity {
    private static final String ZIP_IMPORT_CACHE_DIR = "zip-imports";
    private static final String ZIP_MIME_TYPE = "application/zip";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Intent preparedIntent = prepareZipImportIntent(getIntent());

        if (preparedIntent != null) {
            setIntent(preparedIntent);
        }

        super.onCreate(savedInstanceState);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        Intent preparedIntent = prepareZipImportIntent(intent);

        if (preparedIntent != null) {
            setIntent(preparedIntent);
            super.onNewIntent(preparedIntent);
            return;
        }

        if (intent != null) {
            setIntent(intent);
        }

        super.onNewIntent(intent);
    }

    private Intent prepareZipImportIntent(Intent intent) {
        Uri sourceUri = getZipImportUri(intent);

        if (sourceUri == null) {
            return null;
        }

        if (isCachedImportUri(sourceUri)) {
            return intent;
        }

        try {
            File cachedZip = copyZipToCache(sourceUri);
            Uri cachedUri = Uri.fromFile(cachedZip);
            Intent preparedIntent = new Intent(Intent.ACTION_VIEW);

            preparedIntent.setDataAndType(cachedUri, ZIP_MIME_TYPE);
            preparedIntent.addCategory(Intent.CATEGORY_DEFAULT);

            return preparedIntent;
        } catch (IOException ignored) {
            return null;
        }
    }

    private Uri getZipImportUri(Intent intent) {
        if (intent == null) {
            return null;
        }

        String action = intent.getAction();

        if (Intent.ACTION_VIEW.equals(action)) {
            Uri uri = intent.getData();
            return isZipUri(uri, intent.getType()) ? uri : null;
        }

        if (Intent.ACTION_SEND.equals(action)) {
            Uri streamUri = getSingleStreamUri(intent);

            if (isZipUri(streamUri, intent.getType())) {
                return streamUri;
            }
        }

        if (Intent.ACTION_SEND_MULTIPLE.equals(action)) {
            for (Uri uri : getMultipleStreamUris(intent)) {
                if (isZipUri(uri, intent.getType())) {
                    return uri;
                }
            }
        }

        return null;
    }

    private Uri getSingleStreamUri(Intent intent) {
        Parcelable stream = intent.getParcelableExtra(Intent.EXTRA_STREAM);

        if (stream instanceof Uri) {
            return (Uri) stream;
        }

        ClipData clipData = intent.getClipData();

        if (clipData != null && clipData.getItemCount() > 0) {
            return clipData.getItemAt(0).getUri();
        }

        return null;
    }

    private ArrayList<Uri> getMultipleStreamUris(Intent intent) {
        ArrayList<Uri> uris = intent.getParcelableArrayListExtra(Intent.EXTRA_STREAM);

        if (uris != null && !uris.isEmpty()) {
            return uris;
        }

        ArrayList<Uri> clipUris = new ArrayList<>();
        ClipData clipData = intent.getClipData();

        if (clipData == null) {
            return clipUris;
        }

        for (int index = 0; index < clipData.getItemCount(); index++) {
            Uri uri = clipData.getItemAt(index).getUri();

            if (uri != null) {
                clipUris.add(uri);
            }
        }

        return clipUris;
    }

    private boolean isZipUri(Uri uri, String intentMimeType) {
        if (uri == null) {
            return false;
        }

        String displayName = getDisplayName(uri).toLowerCase(Locale.ROOT);
        String resolverMimeType = getMimeType(uri);
        String mimeType = resolverMimeType != null ? resolverMimeType : intentMimeType;

        return displayName.endsWith(".zip") || isZipMimeType(mimeType);
    }

    private boolean isCachedImportUri(Uri uri) {
        if (!"file".equals(uri.getScheme()) || uri.getPath() == null) {
            return false;
        }

        File importRoot = new File(getCacheDir(), ZIP_IMPORT_CACHE_DIR);
        return uri.getPath().startsWith(importRoot.getAbsolutePath());
    }

    private String getMimeType(Uri uri) {
        try {
            return getContentResolver().getType(uri);
        } catch (RuntimeException ignored) {
            return null;
        }
    }

    private boolean isZipMimeType(String mimeType) {
        if (mimeType == null) {
            return false;
        }

        return mimeType.toLowerCase(Locale.ROOT).contains("zip");
    }

    private File copyZipToCache(Uri sourceUri) throws IOException {
        File importRoot = new File(getCacheDir(), ZIP_IMPORT_CACHE_DIR);
        recreateDirectory(importRoot);

        File importDir = new File(importRoot, String.valueOf(System.currentTimeMillis()));

        if (!importDir.mkdirs() && !importDir.isDirectory()) {
            throw new IOException("Unable to create import cache directory");
        }

        String fileName = sanitizeFileName(getDisplayName(sourceUri));

        if (!fileName.toLowerCase(Locale.ROOT).endsWith(".zip")) {
            fileName = fileName + ".zip";
        }

        File targetFile = new File(importDir, fileName);

        try (InputStream inputStream = getContentResolver().openInputStream(sourceUri);
             FileOutputStream outputStream = new FileOutputStream(targetFile)) {
            if (inputStream == null) {
                throw new IOException("Unable to open shared zip");
            }

            byte[] buffer = new byte[8192];
            int bytesRead;

            while ((bytesRead = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }
        }

        return targetFile;
    }

    private String getDisplayName(Uri uri) {
        if (uri == null) {
            return "whatsapp-chat";
        }

        if ("content".equals(uri.getScheme())) {
            try (Cursor cursor = getContentResolver().query(uri, null, null, null, null)) {
                if (cursor != null && cursor.moveToFirst()) {
                    int nameIndex = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);

                    if (nameIndex >= 0) {
                        String displayName = cursor.getString(nameIndex);

                        if (displayName != null && !displayName.trim().isEmpty()) {
                            return displayName;
                        }
                    }
                }
            } catch (RuntimeException ignored) {
                return "whatsapp-chat";
            }
        }

        String path = uri.getPath();

        if (path == null || path.trim().isEmpty()) {
            return "whatsapp-chat";
        }

        int lastSeparatorIndex = path.lastIndexOf('/');
        return lastSeparatorIndex >= 0 ? path.substring(lastSeparatorIndex + 1) : path;
    }

    private String sanitizeFileName(String fileName) {
        String sanitized = fileName == null ? "" : fileName.trim().replaceAll("[\\\\/:*?\"<>|]+", "-");

        if (sanitized.isEmpty() || ".".equals(sanitized) || "..".equals(sanitized)) {
            return "whatsapp-chat.zip";
        }

        return sanitized;
    }

    private void recreateDirectory(File directory) throws IOException {
        deleteRecursively(directory);

        if (!directory.mkdirs() && !directory.isDirectory()) {
            throw new IOException("Unable to create cache directory");
        }
    }

    private void deleteRecursively(File file) {
        if (file == null || !file.exists()) {
            return;
        }

        if (file.isDirectory()) {
            File[] children = file.listFiles();

            if (children != null) {
                for (File child : children) {
                    deleteRecursively(child);
                }
            }
        }

        file.delete();
    }
}
